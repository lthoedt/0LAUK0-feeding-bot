import time
import RPi.GPIO as GPIO
import pigpio

import threading
import queue
from Component import Component

targetAngleQueue = queue.Queue()
currentAngleQueue = queue.Queue()

class ServoWrapper(Component):
    currentAngle = 0
    previousMillis = 0

    def __init__(self, pin, speed) -> None:
        self.pin = pin
        self.speed = self.mapSpeedToMillis(speed)

        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(self.pin, 50)

        super().__init__()
        
    # 1 is 0 delay, 0 is 40 milliseconds
    def mapSpeedToMillis(self, speed) -> float:
        return (1 - speed) * 80

    def mapAngleToDutyCycle(self, angle) -> float:
        return (angle / 180) * 2000 + 500

    def goToAngle(self, angle):
        self.use(angle)

    # Returns true if done
    def run(self, angle) -> bool:
        # Servo needs to be moved
        if (angle != None and angle != self.currentAngle):
            if ( angle > self.currentAngle ):
                self.currentAngle += 1
            else:
                self.currentAngle -= 1
            self.pwm.set_servo_pulsewidth( self.pin, self.mapAngleToDutyCycle(self.currentAngle) )
            time.sleep(self.speed / 1000)
            print(self.currentAngle)
        else:
            # Servo is done moving
            self.pwm.set_PWM_dutycycle( self.pin, 0 )
            self.pwm.set_PWM_frequency( self.pin, 0 )

        return angle == self.currentAngle