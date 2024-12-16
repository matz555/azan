import subprocess
import sys
import signal

# Senarai stesen radio (dikemas kini)
RADIOS = {
    1: ("Suria FM", "https://22273.live.streamtheworld.com/SURIA_FMAAC.aac"),
    2: ("Sinar FM", "https://radio.garden/api/ara/content/listen/0zQ22YW5/channel.mp3?1732677251772"),
    3: ("Hot FM", "https://stream.rcs.revma.com/drakdf8mtd3vv/3_17mp5oakmwcj602/playlist.m3u8"),
    4: ("Zayan", "https://radio.garden/api/ara/content/listen/UMAAglgc/channel.mp3?1732677185902"),
    5: ("Kool 101", "https://stream.rcs.revma.com/3930238mtd3vv/8_3zp9p15w8eel02/playlist.m3u8"),
    6: ("Kedah FM", "https://22253.live.streamtheworld.com/KEDAH_FMAAC.aac"),
    7: ("Quran Radio", "https://qurango.net/radio/tarateel"),
    8: ("Makkah Live", "https://www.youtube.com/watch?v=PASySDRC31E"),
}

def display_menu():
    print("\nPilih stesen radio untuk dimainkan:")
    for key, (name, _) in RADIOS.items():
        print(f"{key}. {name}")

def play_radio(name, url, volume):
    print(f"\nMemainkan {name} pada volume {volume}%...\nTekan Ctrl+C untuk hentikan.")
    while True:
        try:
            if "youtube" in url:  # Jika URL adalah YouTube
                process = subprocess.Popen(
                    ["yt-dlp", "-f", "bestaudio", "-o", "-", url],
                    stdout=subprocess.PIPE
                )
                player = subprocess.Popen(
                    ["mpv", "--volume", str(volume), "-"],
                    stdin=process.stdout
                )
                player.wait()  # Tunggu sehingga pemain selesai
                process.terminate()
            else:  # URL biasa
                process = subprocess.Popen(
                    ["mpv", f"--volume={volume}", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                process.wait()  # Tunggu sehingga proses selesai
        except KeyboardInterrupt:
            print("\nMenghentikan radio...")
            process.terminate()
            process.wait()
            break
        except Exception as e:
            print(f"Ralat berlaku: {e}. Memulakan semula dalam 5 saat...")
            time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].startswith("vol="):
        print("Usage: play_radio.py vol=<volume (0-100)>")
        sys.exit(1)

    try:
        # Dapatkan nilai volume dari argumen
        volume = int(sys.argv[1].split("=")[1])
        if not (0 <= volume <= 100):
            raise ValueError
    except ValueError:
        print("Error: Volume mesti antara 0 dan 100.")
        sys.exit(1)

    while True:
        display_menu()
        try:
            choice = int(input("\nMasukkan pilihan anda (nombor): "))
            if choice in RADIOS:
                name, url = RADIOS[choice]
                play_radio(name, url, volume)
            else:
                print("Pilihan tidak sah. Sila cuba lagi.")
        except ValueError:
            print("Masukkan nombor yang sah!")
        except KeyboardInterrupt:
            print("\nKeluar dari menu. Selamat tinggal!")
            sys.exit(0)
