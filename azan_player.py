#!/usr/bin/env python

import json
import os
import random
import datetime

def load_prayer_times():
    try:
        year = datetime.datetime.now().year
        file_path = f"/home/pi/waktu_solat_{year}.json"
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

def play_random_azan(subuh=False):
    folder = "/home/pi/azan_audio/azan_subuh" if subuh else "/home/pi/azan_audio/azan_biasa"
    files = [f for f in os.listdir(folder) if f.endswith('.wav')]
    if files:
        file_to_play = os.path.join(folder, random.choice(files))
        play_audio(file_to_play)

def play_doa_selapas_azan():
    doa_path = "/home/pi/azan_audio/doa_selapas_azan/doa.wav"
    play_audio(doa_path)

def play_doa_dhuha():
    doa_dhuha_path = "/home/pi/azan_audio/doa_dhuha/doa_dhuha.wav"
    play_audio(doa_dhuha_path)

def play_audio_isyraq():
    isyraq_path = "/home/pi/azan_audio/isyraq/isyraq.wav"
    play_audio(isyraq_path)

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

if __name__ == "__main__":
    check_and_play_azan()

