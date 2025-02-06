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

    today = datetime.datetime.now().strftime("%d-%b-%Y")

    for entry in data.get('prayerTime', []):
        if entry.get('date') == today:
            for key in ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha', 'syuruk']:
                if key in entry:
                    entry[key] = entry[key][:5]  # Keep only "HH:MM"
            return entry

    print("Error: Today's prayer times not found in JSON data.")
    return None

def set_volume(volume_percentage):
    os.system(f"amixer set Master {volume_percentage}%")

def play_audio(file_path, volume_percentage=100):
    original_volume = 100  # Assume default volume is 100%
    set_volume(volume_percentage)  # Set desired volume
    os.system(f"aplay {file_path}")  # Play audio
    set_volume(original_volume)  # Reset volume

def play_random_audio(folder, volume_percentage=100):
    files = [f for f in os.listdir(folder) if f.endswith('.wav')]
    if files:
        file_to_play = os.path.join(folder, random.choice(files))
        play_audio(file_to_play, volume_percentage)

def play_random_azan(subuh=False):
    folder = "/home/pi/azan/azan_audio/azan_subuh" if subuh else "/home/pi/azan/azan_audio/azan_biasa"
    play_random_audio(folder, volume_percentage=100)

def play_doa_selapas_azan():
    doa_folder = "/home/pi/azan/azan_audio/doa_selapas_azan"
    play_random_audio(doa_folder, volume_percentage=100)

def calculate_extra_times(prayer_times):
    fajr_time = datetime.datetime.strptime(prayer_times['fajr'], "%H:%M")
    syuruk_time = datetime.datetime.strptime(prayer_times['syuruk'], "%H:%M")

    isyraq_time = syuruk_time + datetime.timedelta(minutes=15)
    difference = syuruk_time - fajr_time
    dhuha_time = syuruk_time + datetime.timedelta(seconds=(difference.total_seconds() / 3))

    prayer_times['isyraq'] = isyraq_time.strftime("%H:%M")
    prayer_times['dhuha'] = dhuha_time.strftime("%H:%M")
    return prayer_times

def check_and_play_azan():
    prayer_times = get_today_prayer_times()
    if prayer_times:
        prayer_times = calculate_extra_times(prayer_times)
        now = datetime.datetime.now().strftime("%H:%M")

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
        elif now == prayer_times['dhuha']:
            play_audio("/home/pi/azan/azan_audio/doa_dhuha.wav")
        elif now == prayer_times['isyraq']:
            play_audio("/home/pi/azan/azan_audio/isyraq.wav")

def play_scheduled_zikir():
    zikir_folder = "/home/pi/azan/azan_audio/zikir"
    zikir_schedule = {
        "07:00": "1.wav", "08:00": "2.wav", "09:00": "3.wav", "10:00": "4.wav",
        "11:00": "5.wav", "12:00": "6.wav", "13:00": "7.wav", "14:00": "8.wav",
        "15:00": "9.wav", "16:00": "10.wav", "17:00": "11.wav", "18:00": "12.wav",
        "20:00": "14.wav", "21:00": "15.wav", "22:00": "16.wav", "23:00": "17.wav"
    }

    now = datetime.datetime.now().strftime("%H:%M")
    if now in zikir_schedule:
        play_audio(os.path.join(zikir_folder, zikir_schedule[now]))
    else:
        prayer_times = get_today_prayer_times()
        if prayer_times:
            fifteen_before_maghrib = (datetime.datetime.strptime(prayer_times['maghrib'], "%H:%M") - datetime.timedelta(minutes=15)).strftime("%H:%M")
            fifteen_before_fajr = (datetime.datetime.strptime(prayer_times['fajr'], "%H:%M") - datetime.timedelta(minutes=15)).strftime("%H:%M")
            if now == fifteen_before_maghrib:
                play_audio(os.path.join(zikir_folder, "13.wav"))
            elif now == fifteen_before_fajr:
                play_audio(os.path.join(zikir_folder, "18.wav"))

if __name__ == "__main__":
    check_and_play_azan()
    play_scheduled_zikir()
