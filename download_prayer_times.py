import requests
import datetime

def download_prayer_times():
    url = "https://www.e-solat.gov.my/index.php?r=esolatApi/takwimsolat&period=year&zone=KDH01"
    response = requests.get(url)
    if response.status_code == 200:
        year = datetime.datetime.now().year
        filename = f"/home/pi/waktu_solat_{year}.json"
        with open(filename, "w") as file:
            file.write(response.text)
        print(f"Waktu solat untuk tahun {year} disimpan sebagai {filename}")
    else:
        print("Gagal memuat turun data waktu solat.")

if __name__ == "__main__":
    download_prayer_times()

