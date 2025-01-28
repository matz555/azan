import json
import os
import random
import datetime
import requests

def load_zone_from_file(filepath):
    try:
        with open(filepath, "r") as file:
            zone = file.read().strip()
            return zone
    except FileNotFoundError:
        print("Fail zon tidak ditemui. Sila pastikan fail wujud.")
        return None

def download_prayer_times():
    zone_file = "/home/pi/backup_azan/zone.txt"  # Lokasi fail zon
    zone = load_zone_from_file(zone_file)

    if zone:
        url = f"https://www.e-solat.gov.my/index.php?r=esolatApi/takwimsolat&period=year&zone={zone}"
        response = requests.get(url)
        if response.status_code == 200:
            year = datetime.datetime.now().year
            filename = f"/home/pi/azan/waktu_solat_{year}.json"
            with open(filename, "w") as file:
                file.write(response.text)
            print(f"Waktu solat untuk zon {zone} tahun {year} disimpan sebagai {filename}")
        else:
            print("Gagal memuat turun data waktu solat.")
    else:
        print("Zon waktu solat tidak sah. Program dihentikan.")

def load_prayer_times():
    try:
        year = datetime.datetime.now().year
        file_path = f"/home/pi/azan/waktu_solat_{year}.json"
        if not os.path.exists(file_path):
            print("Fail JSON waktu solat tidak dijumpai. Memuat turun fail...")
            download_prayer_times()
        
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: Prayer times JSON file not found selepas percubaan memuat turun.")
        return None
    except json.JSONDecodeError:
        print("Error: JSON file is not formatted correctly.")
        return None

def get_today_prayer_times():
    data = load_prayer_times()
    if data is None:
        return None

    # Format today's date to match JSON format, e.g., 01-Nov-2024
    today = datetime.datetime.now().strftime("%d-%b-%Y")
    
    # Loop through each entry in prayerTime and match the date
    for entry in data.get('prayerTime', []):
        if entry.get('date') == today:
            # Remove seconds from each prayer time
            for key in ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha', 'syuruk']:
                if key in entry:
                    entry[key] = entry[key][:5]  # Keep only "HH:MM"
            return entry

    print("Error: Today's prayer times not found in JSON data.")
    return None

def play_audio(file_path):
    os.system(f"aplay {file_path}")

def play_random_audio(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.wav')]
    if files:
        file_to_play = os.path.join(folder, random.choice(files))
        play_audio(file_to_play)

def play_random_azan(subuh=False):
    folder = "/home/pi/azan/azan_audio/azan_subuh" if subuh else "/home/pi/azan/azan_audio/azan_biasa"
    play_random_audio(folder)

def play_doa_selapas_azan():
    doa_path = "/home/pi/azan/azan_audio/doa_selapas_azan/doa.wav"
    play_audio(doa_path)

def play_doa_dhuha():
    doa_dhuha_path = "/home/pi/azan/azan_audio/doa_dhuha/doa_dhuha.wav"
    play_audio(doa_dhuha_path)

def play_audio_isyraq():
    isyraq_path = "/home/pi/azan/azan_audio/isyraq/isyraq.wav"
    play_audio(isyraq_path)

def play_surah_almulk():
    almulk_path = "/home/pi/azan/azan_audio/surah_almulk.wav"
    play_audio(almulk_path)

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

def check_and_play_azan():
    prayer_times = get_today_prayer_times()
    if prayer_times:
        prayer_times = calculate_extra_times(prayer_times)
        now = datetime.datetime.now().strftime("%H:%M")  # Only hours and minutes
        
        if now == prayer_times['fajr']:
            play_random_azan(subuh=True)
            play_doa_selapas_azan()
        elif now == prayer_times['dhuhr']:
            play_random_azan()
            play_doa_selapas_azan()
        elif now == prayer_times['asr']:
            play_random_azan()
            play_doa_selapas_azan()
        elif now == prayer_times['maghrib']:
            play_random_azan()
            play_doa_selapas_azan()
        elif now == prayer_times['isha']:
            play_random_azan()
            play_doa_selapas_azan()
        elif now == prayer_times['isyraq']:
            play_audio_isyraq()
        elif now == prayer_times['dhuha']:
            play_doa_dhuha()

def check_and_play_surah_almulk():
    now = datetime.datetime.now().strftime("%H:%M")
    if now == "22:10":  # 10:10 PM
        play_surah_almulk()

def set_volume(volume_percentage):
    """Set system volume to the specified percentage."""
    os.system(f"amixer set Master {volume_percentage}%")

def play_audio(file_path, volume_percentage=100):
    """Play audio with specified volume, then reset to 100%."""
    original_volume = 100  # Assume default volume is 100%
    set_volume(volume_percentage)  # Set desired volume
    os.system(f"aplay {file_path}")  # Play audio
    set_volume(original_volume)  # Reset volume

def play_random_audio(folder, volume_percentage=100):
    """Play a random audio file from a folder with specified volume."""
    files = [f for f in os.listdir(folder) if f.endswith('.wav')]
    if files:
        file_to_play = os.path.join(folder, random.choice(files))
        play_audio(file_to_play, volume_percentage)

def check_and_play_zikir():
    now = datetime.datetime.now()
    current_hour = now.strftime("%H")
    current_minute = now.strftime("%M")

    if current_minute == "00":  # Check if it's the start of the hour
        zikir_log_path = "/home/pi/azan/zikir_log.txt"
        #prayer_times = get_today_prayer_times()
        
        # Load or create a log to ensure zikir plays only once per hour
        if os.path.exists(zikir_log_path):
            with open(zikir_log_path, "r") as file:
                zikir_log = file.read().splitlines()
        else:
            zikir_log = []

        # Check if the current hour is already logged
        if current_hour not in zikir_log:
            # Play zikir only between 6:00 AM and 10:00 PM
            if 6 <= int(current_hour) <= 22:
                zikir_folder = "/home/pi/azan/azan_audio/zikir"
                play_random_audio(zikir_folder, volume_percentage=70)  # Play zikir at 70% volume

                # Log the hour
                with open(zikir_log_path, "a") as file:
                    file.write(current_hour + "\n")

        # Clear the log at midnight
        if now.strftime("%H:%M") == "00:00":
            open(zikir_log_path, "w").close()

if __name__ == "__main__":
    check_and_play_azan()
    check_and_play_surah_almulk()
    check_and_play_zikir()
