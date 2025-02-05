import requests
import datetime
import pytz
import os
import time
import smbus

# Konfigurasi untuk RTC DS3231
I2C_BUS = 1  # Bus I2C untuk Raspberry Pi
RTC_ADDRESS = 0x68  # Alamat I2C DS3231

bus = smbus.SMBus(I2C_BUS)

def bcd_to_dec(bcd):
    return (bcd // 16) * 10 + (bcd % 16)

def dec_to_bcd(dec):
    return (dec // 10) * 16 + (dec % 10)

def get_google_time():
    """Dapatkan masa dari Google dan tukarkan ke zon waktu Kuala Lumpur."""
    try:
        response = requests.head("https://www.google.com", timeout=5)
        date_header = response.headers["Date"]
        
        # Tukar string waktu ke objek datetime UTC
        utc_time = datetime.datetime.strptime(date_header, "%a, %d %b %Y %H:%M:%S GMT")
        utc_time = utc_time.replace(tzinfo=pytz.utc)
        
        # Tukar ke zon waktu Malaysia
        kl_time = utc_time.astimezone(pytz.timezone("Asia/Kuala_Lumpur"))
        return kl_time
    except Exception as e:
        print("Ralat mendapatkan masa dari Google:", e)
        return None

def set_system_time(dt):
    """Tetapkan masa sistem Raspberry Pi."""
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    os.system(f'sudo date -s "{formatted_time}"')
    print(f"Masa sistem dikemas kini: {formatted_time}")

def write_rtc_time(dt):
    """Simpan masa ke dalam RTC DS3231."""
    sec = dec_to_bcd(dt.second)
    minute = dec_to_bcd(dt.minute)
    hour = dec_to_bcd(dt.hour)
    day = dec_to_bcd(dt.day)
    month = dec_to_bcd(dt.month)
    year = dec_to_bcd(dt.year - 2000)

    bus.write_byte_data(RTC_ADDRESS, 0x00, sec)
    bus.write_byte_data(RTC_ADDRESS, 0x01, minute)
    bus.write_byte_data(RTC_ADDRESS, 0x02, hour)
    bus.write_byte_data(RTC_ADDRESS, 0x04, day)
    bus.write_byte_data(RTC_ADDRESS, 0x05, month)
    bus.write_byte_data(RTC_ADDRESS, 0x06, year)
    print("Masa telah disimpan ke dalam RTC DS3231.")

def read_rtc_time():
    """Baca masa dari RTC DS3231."""
    sec = bcd_to_dec(bus.read_byte_data(RTC_ADDRESS, 0x00) & 0x7F)
    minute = bcd_to_dec(bus.read_byte_data(RTC_ADDRESS, 0x01))
    hour = bcd_to_dec(bus.read_byte_data(RTC_ADDRESS, 0x02))
    day = bcd_to_dec(bus.read_byte_data(RTC_ADDRESS, 0x04))
    month = bcd_to_dec(bus.read_byte_data(RTC_ADDRESS, 0x05))
    year = bcd_to_dec(bus.read_byte_data(RTC_ADDRESS, 0x06)) + 2000

    dt = datetime.datetime(year, month, day, hour, minute, sec)
    print(f"Masa dari RTC DS3231: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    return dt

def sync_time():
    """Sync masa sistem dari internet atau RTC DS3231."""
    kl_time = get_google_time()
    
    if kl_time:
        print("Berjaya mendapatkan masa dari internet.")
        set_system_time(kl_time)
        write_rtc_time(kl_time)
    else:
        print("Tiada sambungan internet. Menggunakan masa dari RTC DS3231.")
        rtc_time = read_rtc_time()
        set_system_time(rtc_time)

# Jalankan sync masa
sync_time()

