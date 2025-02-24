import requests
import datetime
import pytz
import os

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

def sync_time():
    """Sync masa sistem dari internet."""
    kl_time = get_google_time()
    
    if kl_time:
        print("Berjaya mendapatkan masa dari internet.")
        set_system_time(kl_time)
    else:
        print("Tiada sambungan internet. Tidak dapat mengemas kini masa.")

# Jalankan sync masa
sync_time()
