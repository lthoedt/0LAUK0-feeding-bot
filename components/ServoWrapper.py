import time
import RPi.GPIO as GPIO
import pigpio

class ServoWrapper:
    currentAngle = 0
    previousMillis = 0

    def __init__(self, pin, speed) -> None:
        self.pin = pin
        self.speed = self.mapSpeedToMillis(speed)

        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(self.pin, 50)

    # 1 is 0 delay, 0 is 40 milliseconds
    def mapSpeedToMillis(self, speed) -> int:
        return (1 - speed) * 40

    def mapAngleToDutyCycle(self, angle) -> Number:
        return (angle / 180) * 2000 + 500

    def goToAngle(self, angle):
        currentMillis = time.time_ns() // 1_000_000

        if ( currentMillis >= (self.previousMillis + self.speed) ):
            if (angle != self.currentAngle):
                if ( angle > self.currentAngle ):
                    self.currentAngle += 1
                else:
                    self.currentAngle -= 1
            else:
                self.pwm.set_PWM_dutycycle( self.pin, 0 )
                self.pwm.set_PWM_frequency( self.pin, 0 )
            self.previousMillis = currentMillis
        
        self.pwm.set_servo_pulsewidth( self.pin, self.mapAngleToDutyCycle(self.currentAngle) )

        return self.currentAngle == angle
