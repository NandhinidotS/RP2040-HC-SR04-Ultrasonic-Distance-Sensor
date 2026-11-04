from machine import Pin, time_pulse_us
import time

trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

DETECT_LIMIT_CM = 30  # object counts as "present" if closer than this

def get_distance_cm():
    # Send a 10 microsecond pulse on trig
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Measure how long echo stays high (timeout 30 ms)
    duration = time_pulse_us(echo, 1, 30000)

    if duration < 0:
        return None  # no echo received

    # Sound speed: 0.0343 cm/us, divide by 2 for round trip
    return (duration * 0.0343) / 2

print("HC-SR04 distance sensor started")

while True:
    distance = get_distance_cm()

    if distance is None:
        print("No echo - check wiring")
    elif distance < DETECT_LIMIT_CM:
        print("Object PRESENT | Distance: {:.1f} cm".format(distance))
    else:
        print("No object nearby | Distance: {:.1f} cm".format(distance))

    time.sleep(0.5)
