import time
from servo import Servo
from Camera import Camera

class ServoWrapper:
    currentAngle = 0
    previousMillis = 0

    def __init__(self, pin, speed) -> None:
        self.pin = pin
        self.speed = speed
        self.servo = Servo(pin_id=pin)

    # 1 is 0 delay, 0 is 40 milliseconds
    def mapSpeedToMillis(self) -> Number:
        return (1 - self.speed) * 40

    def goToAngle(self, angle):
        currentMillis = time.time_ns() // 1_000_000

        if ( currentMillis >= (previousMillis + mapSpeedToMillis()) ):
            if (angle != self.currentAngle):
                if ( angle > servoCurrentAngle ):
                    servoCurrentAngle += 1
                else :
                    servoCurrentAngle -= 1
        
            previousMillis = currentMillis
        
        servo.write( servoCurrentAngle )

        return servoCurrentAngle == angle
