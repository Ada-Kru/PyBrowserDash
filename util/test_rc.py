import serial
import time

with serial.Serial("COM3", 9600, timeout=3) as ser:
    time.sleep(2.1)
    ser.write(b'1_1_06\n')
