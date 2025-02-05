import smbus
import time

# Alamat I2C DS3231
DS3231_ADDR = 0x68
bus = smbus.SMBus(1)

def bcd_to_dec(bcd):
    """Tukar nilai BCD ke format decimal."""
    return (bcd // 16) * 10 + (bcd % 16)

def read_time():
    """Baca masa dari DS3231."""
    data = bus.read_i2c_block_data(DS3231_ADDR, 0x00, 7)
    seconds = bcd_to_dec(data[0])
    minutes = bcd_to_dec(data[1])
    hours = bcd_to_dec(data[2])
    day = bcd_to_dec(data[4])
    month = bcd_to_dec(data[5])
    year = bcd_to_dec(data[6]) + 2000

    return f"{year}-{month:02d}-{day:02d} {hours:02d}:{minutes:02d}:{seconds:02d}"

while True:
    print("Masa RTC:", read_time())
    time.sleep(1)

