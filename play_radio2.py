import os
import subprocess
import sys
import argparse

# Senarai stesen radio
stations = {
    "1": ("Suria FM", "https://22273.live.streamtheworld.com/SURIA_FMAAC.aac"),
    "2": ("Sinar FM", "https://radio.garden/api/ara/content/listen/0zQ22YW5/channel.mp3"),
    "3": ("Hot FM", "https://stream.rcs.revma.com/drakdf8mtd3vv/3_17mp5oakmwcj602/playlist.m3u8"),
    "4": ("Zayan", "https://radio.garden/api/ara/content/listen/UMAAglgc/channel.mp3"),
    "5": ("Kool 101", "https://stream.rcs.revma.com/3930238mtd3vv/8_3zp9p15w8eel02/playlist.m3u8"),
    "6": ("Kedah FM", "https://22253.live.streamtheworld.com/KEDAH_FMAAC.aac"),
    "7": ("Quran Radio", "https://qurango.net/radio/tarateel"),
    "8": ("Makkah Live", "https://n08.radiojar.com/0tpy1h0kxtzuv?rj-ttl=5&rj-tok=AAABk_kzCAkArD78rdQiH0hHsw"),
}

def set_volume(volume_level):
    """Tetapkan volume menggunakan amixer."""
    try:
        subprocess.run(["amixer", "sset", "Master", f"{volume_level}%"], check=True)
        print(f"Volume ditetapkan kepada {volume_level}%.")
    except Exception as e:
        print(f"Gagal menetapkan volume: {e}")

def play_station(station_url, is_youtube=False):
    """Mainkan stesen radio menggunakan mpv."""
    try:
        if is_youtube:
            subprocess.run(["mpv", "--no-video", station_url], check=True)
        else:
            subprocess.run(["mpv", station_url], check=True)
    except KeyboardInterrupt:
        print("\nStreaming dihentikan.")
    except Exception as e:
        print(f"Ralat: {e}")

def main():
    # Parser argumen
    parser = argparse.ArgumentParser(description="Player Radio")
    parser.add_argument("--vol", type=int, help="Tahap volume (1-100)")
    args = parser.parse_args()

    # Tetapkan volume jika diberikan
    if args.vol:
        if 1 <= args.vol <= 100:
            set_volume(args.vol)
        else:
            print("Tahap volume mestilah antara 1 hingga 100.")
            sys.exit(1)

    # Paparkan menu
    print("Senarai Stesen Radio:")
    for key, (name, _) in stations.items():
        print(f"{key}. {name}")
    print("\nMasukkan nombor pilihan stesen radio (contoh: 1) atau 'q' untuk keluar.")

    try:
        choice = input("Pilihan anda: ").strip()
        if choice.lower() == 'q':
            print("Keluar.")
            sys.exit(0)

        if choice in stations:
            station_name, station_url = stations[choice]
            is_youtube = "youtube.com" in station_url
            print(f"Anda memilih: {station_name}")
            print(f"Sedang memainkan {station_name}...")
            play_station(station_url, is_youtube)
        else:
            print("Pilihan tidak sah.")
            sys.exit(1)

    finally:
        # Pastikan volume dikembalikan ke 100% apabila skrip tamat
        print("Mengembalikan volume kepada 100%...")
        set_volume(100)

if __name__ == "__main__":
    main()
