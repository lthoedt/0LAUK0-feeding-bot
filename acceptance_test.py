from components import Classifier
from components import Camera
from components import Door
from components import ServoWrapper

from MainSystem import MainSystem
from States import States
import StateMethods

import logging


global _tests
_tests = []


def test(fun):
    global _tests

    kvs = [
        list(filter(None, line.strip().split(":")))
        for line in fun.__doc__.strip().split("\n")
    ]
    print(kvs)
    docs = {kv[0].strip(): (kv[1].strip() if len(kv) > 1 else "") for kv in kvs}

    def wrapper():
        print(f"Running test {fun.__name__} ...")
        print(f"> Requirement: {docs['Requirement']}")
        print(f"> Precondition: {docs['Precondition']}")
        print(f"> Action: {docs['Action']}")
        print(f"> Expected Output: {docs['Expected Output']}")
        fun()
        input("Press Enter to continue to next test or Ctrl-C to quit ...\n")

    _tests += [wrapper]
    return wrapper


@test
def test_servomotor():
    """
    Requirement:		Servomotor works
    Precondition:		Servomotor is on
    Action:		Signal is given to servomotor
    Expected Output:		Servomotor changes from its initial state
    """

    print("Turning on servo ...")
    servo = ServoWrapper(12, 0.4)

    print("Move to 30°")
    servo.goToAngle(30)
    time.sleep(0.1)
    while not servo.getResult():
        time.sleep(0.1)
    print("Move to 60°")
    servo.goToAngle(60)
    time.sleep(0.1)
    while not servo.getResult():
        time.sleep(0.1)

    print("Turning off ...")
    servo.pwm.set_PWM_dutycycle(servo, 0)
    servo.pwm.set_PWM_frequency(servo, 0)


@test
def test_camera():
    """
    Requirement:		Camera works
    Precondition:		Camera is on
    Action:		Camera is connected to laptop
    Expected Output:		Recordings from camera can be seen on the laptop
    """

    print("Turning on camera ...")
    camera = Camera()
    print("Taking picture ...")
    camera.takePicture()
    while not camera.getResult():
        time.sleep(0.1)
    print("Storing image:")
    camera.getResult().save("~/test_image.jpg")
    print("To view image, copy the file ~/test_image.jpg from the pi")
    camera.picamera.stop()


@test
def test_bird_identification():
    """
    Requirement:		The subsystem can detect 4 types of birds from printed images
    Precondition:		Detection system is on
    Action:		        an image of a bird is shown
    Expected Output:	Identification system reports type of bird correctly
    """

    print("Turning on camera and classifier ...")
    camera = Camera()
    classifier = Classifier()

    print("Processing images from camera, press Ctrl-C once when done ...")
    try:
        while True:
            camera.takePicture()
            img = camera.getImage()
            if img:
                classifier.scanImage(img)

            c = classifier.getResult()
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass

    camera.picamera.stop()


@test
def test_door_opening_and_closing():
    """
    Requirement:		Door can open and close
    Precondition:		Servomotor is powered on
    Action:		        Door gets order to close
    Expected Output:	Door closes and after 30 seconds opens
    """
    system = MainSystem()
    system.CURRENT_STATE = States.DENYING_BIRD
    StateMethods.DenyingBirdState.entry(system)

    print("Door should be closed; waiting 30 seconds ...")
    time.sleep(30.1)
    print("Continue if door was opened again")
    system.camera.picamera.stop()
    system.door.servo.pwm.set_PWM_dutycycle(servo, 0)
    system.door.servo.pwm.set_PWM_frequency(servo, 0)


@test
def test_bird_stuck_prevention():
    """
    Requirement:		Door can open and close without leaving too much space for a bird to get stuck
    Precondition:		Servomotor is powered on
    Action:		        The door opens and closes
    Expected Output:	The door closes without ever leaving more than 2 cm of space
    """
    door = Door()

    for i in range(2):
        print("Opening ...")
        door.open()
        time.sleep(4)
        print("Closing ...")
        door.close()
        time.sleep(4)

    door.servo.pwm.set_PWM_dutycycle(servo, 0)
    door.servo.pwm.set_PWM_frequency(servo, 0)


@test
def test_bird_crushed_prevention():
    """
    Requirement:		The door can open and close without birds getting stuck
    Precondition:		Servomotor is powered on
    Action:		The door opens and closes
    Expected Output:		The door closes in 4 seconds leaving enough time for the bird to fly away
    """
    door = Door()

    for i in range(2):
        print("Opening ...")
        door.open()
        time.sleep(4)
        print("Closing ...")
        door.close()
        time.sleep(4)

    door.servo.pwm.set_PWM_dutycycle(servo, 0)
    door.servo.pwm.set_PWM_frequency(servo, 0)


@test
def test_undesired_bird_prevention_test():
    """
    Requirement:		The robot prevents classified undesired birds from feeding
    Precondition:		Robot is outside for multiple days, powered on, has feed in its storage compartment and sends pictures to a laptop to confirm the test is completed
    Action:		        undesired Birds come and feed at the robot.
    Expected Output:	The robot closes the door for undesired birds
    """
    system = MainSystem()

    print("Main System running")
    print("Test considered successful if door closes after a denied bird was shown")
    while not system.CURRENT_STATE == States.DENYING_BIRD and not system.door.isClosed():
        system.loop()
        time.sleep(0.2)

    system.camera.picamera.stop()
    system.door.servo.pwm.set_PWM_dutycycle(servo, 0)
    system.door.servo.pwm.set_PWM_frequency(servo, 0)


def main():
    print("Running all tests ...")
    print()

    for test in _tests:
        test()

    print()
    print("Done!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
