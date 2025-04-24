import network  # MicroPython-Netzwerktreiber
import socket
import time

from imu import MPU6050  # https://github.com/micropython-IMU/micropython-mpu9x50
import math
from machine import Pin, I2C, Timer

counter = 0
DELAY = 5

"""
timer_task wird periodisch aufgerufen und
sendet Sensordaten an den im "Hauptprogramm"
definierten TCP-Socket.
"""
def timer_task(t):
    global counter
    counter += 1
    acceleration = imu.accel
    gyroscope = imu.gyro
    ax = acceleration.x
    ay = acceleration.y
    az = acceleration.z
    gx = gyroscope.x
    gy = gyroscope.y
    gz = gyroscope.z
    sensor_data = b'{"n":%d, "ax":%f, "ay":%f, "az":%f, "gx":%f, "gy":%f, "gz":%f}\n' % (counter, ax, ay, az, gx, gy, gz)
    s.sendall(sensor_data)
#################################################################################

# Aktivierung des Gyro-Sensors
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

# Verbindung zum WLAN aufbauen
ssid = 'jetson03'
password = 'Alea iacta est!'

network.country('DE')
wlan = network.WLAN(network.STA_IF) # WLAN-Objekt als Client konfigiriert
wlan.active(True)                   # WLAN aktivieren
# wlan.ifconfig(('192.168.0.50','255.255.255.0','192.168.0.1','192.168.0.1'))
wlan.connect(ssid, password)        # Verbindungsaufbau zum Accesspoint

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
# Verbindung zum Zielrechner aufbauen    
addr = socket.getaddrinfo('10.42.0.1', 5005)[0][-1]  # IPv4-Socket-Adresse erzeugen

s = socket.socket()
s.connect(addr)

# Timer initialisieren
timer = Timer(period=DELAY, mode=Timer.PERIODIC, callback=timer_task)

# Alle Funktionalität ist im timer_task (s. oben)
while True:
    pass

# Diese Stelle wird nicht mehr erreicht:
s.close()
