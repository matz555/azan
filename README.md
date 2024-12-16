# azan

sudo apt update
sudo apt upgrade
git clone https://github.com/matz555/azan.git
cd /home/pi/azan

copy audio using filezilla

python3 download_prayer_times.py
sudo apt install mpv -y
sudo chmod +x azan_player.py
sudo chmod +x play_radio.py
sudo chmod +x play_radio2.py
sudo chmod +x download_prayer_times.py

sudo crontab -e
0 3 * * * /sbin/shutdown -r now

crontab -e
0 0 1 1 * python3 /home/pi/azan/download_prayer_times.py
* * * * * DISPLAY=:0 XDG_RUNTIME_DIR=/run/user/1000 /usr/bin/python3 /home/pi/azan/azan_player.py
