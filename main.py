from microbit import *
import music
from random import randint
import neopixel
from bitcar import BitCar

def move(bitCar, state, power):
    bitCar.motorL(state, power)
    bitCar.motorR(state, power)

def init():
    np = neopixel.NeoPixel(pin5, 18)
    bitCar = BitCar()
    bitCar.headlights(0, 1, 0)
    for pixel_id in range(0, len(np)):
        np[pixel_id] = (0, 0, 0)
        np.show()
    return bitCar, np

def run():
    bitCar, np = init()
    while True:
        d = bitCar.sonar_distance()
        # display.scroll(str(int(d)))
        if d < 0:
            d = 0
        elif d > 200:
            d = 200
        g = int(255*d/200)
        r = 255 - g
        bitCar.headlights(r, g, 0)

        if d < 20:
            move(bitCar, 0, 128)
        elif d >= 20 and d < 50:
            move(bitCar, 1, 128)
        else:
            move(bitCar, 0, 0)


        sleep(100)


run()









