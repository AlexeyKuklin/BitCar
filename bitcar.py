from microbit import *
from machine import time_pulse_us
import ustruct

class BitCar(object):
    def __init__(self):
        self.add = 0x43
        i2c.write(self.add, bytearray([0x00, 0x00]), repeat=False)
        self.set_all_pwm(0, 0)
        i2c.write(self.add, bytearray([0x01, 0x04]), repeat=False)
        i2c.write(self.add, bytearray([0x00, 0x01]), repeat=False)
        sleep(5)
        i2c.write(self.add, bytearray([0x00]), repeat=False)
        mode1 = i2c.read(self.add, 1)
        mode1 = ustruct.unpack('<B', mode1)[0]
        mode1 = mode1 & ~0x10
        i2c.write(self.add, bytearray([0x00, mode1]), repeat=False)
        sleep(5)

    def set_pwm(self, channel, on, off):
        if on is None or off is None:
            i2c.write(self.add, bytearray([0x06+4*channel]), repeat=False)
            data = i2c.read(self.add, 4)
            return ustruct.unpack('<HH', data)
        i2c.write(self.add, bytearray([0x06+4*channel, on & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x07+4*channel, on >> 8]), repeat=False)
        i2c.write(self.add, bytearray([0x08+4*channel, off & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x09+4*channel, off >> 8]), repeat=False)

    def set_all_pwm(self, on, off):
        i2c.write(self.add, bytearray([0xFA, on & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0xFB, on >> 8]), repeat=False)
        i2c.write(self.add, bytearray([0xFC, off & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0xFD, off >> 8]), repeat=False)

    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

    def motorL(self, state, power):
        p = int(self.map(power, 0, 255, 0, 4095))
        if (state == 1):
            self.set_pwm(0, 0, 0)
            self.set_pwm(1, 0, p)
        elif (state == 0):
            self.set_pwm(0, 4096, 0)
            self.set_pwm(1, 0, p)

    def motorR(self, state, power):
        p = int(self.map(power, 0, 255, 0, 4095))
        if (state == 1):
            self.set_pwm(2, 0, 0)
            self.set_pwm(3, 0, p)
        if (state == 0):
            self.set_pwm(2, 4096, 0)
            self.set_pwm(3, 0, p)

    def headlights(self, R, G, B):
        R = int(4095-(R/255)*4095)
        G = int(4095-(G/255)*4095)
        B = int(4095-(B/255)*4095)
        self.set_pwm(6, 0, R)
        self.set_pwm(5, 0, G)
        self.set_pwm(4, 0, B)
        
    def sonar_distance(self):
        pin14.write_digital(0)
        pin14.write_digital(1)
        t = time_pulse_us(pin15, 1)
        return (t / 2000000)*34300
