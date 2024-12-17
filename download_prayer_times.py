import requests
import datetime

def load_zone_from_file(filepath):
    try:
        with open(filepath, "r") as file:
            zone = file.read().strip()
            return zone
    except FileNotFoundError:
        print("Fail zon tidak ditemui. Sila pastikan fail wujud.")
        return None

def download_prayer_times():
    zone_file = "/home/pi/azan/zone.txt"  # Lokasi fail zon
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

if __name__ == "__main__":
    download_prayer_times()
