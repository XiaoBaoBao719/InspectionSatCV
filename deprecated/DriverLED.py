from os import *
#from gpiozero import LED
from time import sleep
import RPi.GPIO as GPIO
import threading

# =====================================
# ==         GLOBAL VARS         ==
# =====================================
WHITE_LED_PIN = 0 # GPIO 
RGB_PINS = 0 # GPIO

class DriverLED:
    """
    Driver for the S/C LEDs on the flight board.
    """
    board = ""
    
    def __init__(self, boardType):
        self.board = boardType
        self.setBoard()
        print("Board type set to: ", boardType)
        self.initializeLEDs()
        
    def setBoard(self):
        """TODO: Change this function because it doesn't make sense
                having global constants be mutable.
        """
        if self.board == "RPI4":
            WHITE_LED_PIN = 17
            RGB_PINS = [2, 3, 4]

        elif self.board == "CM4":
            WHITE_LED_PIN = 18
            RGB_PINS = 1
            
    def initializeLEDs(self):
        GPIO.setup(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(WHITE_LED_PIN, GPIO.OUT)
        GPIO.setup(RGB_PINS, GPIO.OUT)
        self.blink(5)
        
    def blink(numBlinks):
        for i in range(numBlinks):
            print("White LED ON")
            GPIO.output(WHITE_LED_PIN, GPIO.HIGH)
            sleep(1)
            print("White LED OFF")
            GPIO.output(WHITE_LED_PIN, GPIO.LOW)
            
    def destroy():
        #pwmR.stop()
        #pwmG.stop()
        #pwmB.stop()
        GPIO.cleanup()
    
    