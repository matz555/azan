import datetime
import json

def load_prayer_times():
    """Load prayer times from the local JSON file."""
    try:
        year = datetime.datetime.now().year
        file_path = f"/home/pi/azan/waktu_solat_{year}.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: Prayer times JSON file not found.")
        return None
    except json.JSONDecodeError:
        print("Error: JSON file is not formatted correctly.")
        return None

def get_today_prayer_times():
    """Retrieve today's prayer times from the JSON data."""
    data = load_prayer_times()
    if data is None:
        return None

    today = datetime.datetime.now().strftime("%d-%b-%Y")
    for entry in data.get('prayerTime', []):
        if entry.get('date') == today:
            # Remove seconds from prayer times
            for key in ['fajr', 'syuruk', 'dhuhr', 'asr', 'maghrib', 'isha']:
                if key in entry:
                    entry[key] = entry[key][:5]  # Keep only "HH:MM"
            return calculate_extra_times(entry)

    print("Error: Today's prayer times not found in JSON data.")
    return None

def calculate_extra_times(prayer_times):
    """Calculate Dhuha and Isyraq times based on Syuruk and Fajr."""
    fajr_time = datetime.datetime.strptime(prayer_times['fajr'], "%H:%M")
    syuruk_time = datetime.datetime.strptime(prayer_times['syuruk'], "%H:%M")
    
    # Calculate Isyraq (15 minutes after Syuruk)
    isyraq_time = syuruk_time + datetime.timedelta(minutes=15)
    
    # Calculate Dhuha (Syuruk + 1/3 of (Syuruk - Fajr))
    difference = syuruk_time - fajr_time
    dhuha_time = syuruk_time + datetime.timedelta(seconds=(difference.total_seconds() / 3))
    
    prayer_times['isyraq'] = isyraq_time.strftime("%H:%M")
    prayer_times['dhuha'] = dhuha_time.strftime("%H:%M")
    return prayer_times

def log_special_prayer_times(prayer_times):
    """Identify and log prayer times with specific conditions."""
    log_path = "/home/pi/azan/zikir_log.txt"

    with open(log_path, "a") as log_file:
        for key, time_str in prayer_times.items():
            try:
                if key == "date":
                    continue  # Skip logging the date
                hour, minute = map(int, time_str.split(":"))
                if minute > 50:
                    log_file.write(f"{hour + 1:02d}\n")
                elif minute < 5:
                    log_file.write(f"{hour:02d}\n")
            except ValueError:
                print(f"Invalid time format for {key}: {time_str}")

if __name__ == "__main__":
    prayer_times = get_today_prayer_times()
    if prayer_times:
        log_special_prayer_times(prayer_times)
        print("Special prayer times logged.")
    else:
        print("Unable to process prayer times.")
