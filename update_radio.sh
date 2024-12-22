#!/bin/bash

# Direktori kerja
WORK_DIR="/home/pi/azan"
BACKUP_DIR="$HOME/backup_azan"

# Navigasi ke direktori kerja
cd "$WORK_DIR" || exit

# Buat direktori backup jika belum wujud
mkdir -p "$BACKUP_DIR"

# Tarik kemas kini Git dalam sesi yang sama
echo "Menarik kemas kini dari Git..."
git pull origin main

# Jalankan skrip Python selepas git pull
echo "Menjalankan skrip Python untuk memuat turun waktu solat..."
python3 download_prayer_times.py

# Paparkan mesej selesai
echo "Proses selesai. Fail yang dipindahkan disimpan di $BACKUP_DIR."
