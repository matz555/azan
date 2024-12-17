#!/bin/bash

# Direktori kerja
WORK_DIR="/home/pi/azan"
BACKUP_DIR="$HOME/backup_azan"

# Navigasi ke direktori kerja
cd "$WORK_DIR" || exit

# Buat direktori backup jika belum wujud
mkdir -p "$BACKUP_DIR"

# Periksa fail konflik sebelum git pull
CONFLICT_FILES=("open_terminal.sh" "update_radio.sh")

echo "Memeriksa fail yang mungkin menyebabkan konflik..."

# Pindahkan fail konflik ke direktori backup
for file in "${CONFLICT_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Memindahkan $file ke $BACKUP_DIR/"
        mv -v "$file" "$BACKUP_DIR/"
    fi
done

# Tarik kemas kini Git dalam terminal baharu
echo "Menarik kemas kini dari Git..."
lxterminal -e "bash -c 'git pull origin main; exec bash'"

# Menunggu proses git pull selesai
sleep 5  # Memberi sedikit masa untuk terminal selesai

# Jalankan skrip Python selepas git pull
echo "Menjalankan skrip Python untuk memuat turun waktu solat..."
python3 download_prayer_times.py

# Paparkan mesej selesai
echo "Proses selesai. Fail yang dipindahkan disimpan di $BACKUP_DIR."
