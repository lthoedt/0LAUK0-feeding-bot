import logging
logger = logging.getLogger(__name__)

from States import States
import StateMethods
from config import DRY_RUN, CLOSED_DOOR_TIMEOUT
from components.Camera import Camera, FakeCamera
from components.Classifier import Classifier
from components.Door import Door, FakeDoor

class MainSystem:
    def __init__(self) -> None:
        logger.debug("Initialising main system ...")
        self.CURRENT_STATE = States.SCANNING

        self.classifier = Classifier()
        if not DRY_RUN:
            self.camera = Camera()
            self.door = Door()
        else:
            self.camera = FakeCamera()
            self.door = FakeDoor()

        logger.debug("Finished initialising main system")

    def loop(self) -> None:
        # Instruct camera to take a picture
        self.camera.takePicture()

        # Load the latest image from the camera which can be None if the camera is still busy
        latestImage = self.camera.getImage()

        if latestImage is not None:
            self.classifier.scanImage(latestImage)

        isDeniedBirdDetected : bool | None = self.classifier.getResult()

        # State machine
        # In each case the corresponding State class is called
        # The state class will have an entry, do, and exit method
        # In each case an exit check is performed to determine if the state should change
        # Upon true, the exit method is called and the state is changed to the next state and the entry method is called

        match self.CURRENT_STATE:
            case States.SCANNING:
                StateMethods.ScanningState.do(self)
                if isDeniedBirdDetected:
                    StateMethods.ScanningState.exit(self)
                    self.CURRENT_STATE = States.DENYING_BIRD
                    StateMethods.DenyingBirdState.entry(self)

            case States.ACCEPTING_BIRD:
                # Do
                StateMethods.AcceptingBirdState.do(self)

                if isDeniedBirdDetected:
                    # Exit
                    StateMethods.AcceptingBirdState.exit(self)
                    self.CURRENT_STATE = States.DENYING_BIRD
                    StateMethods.DenyingBirdState.entry(self)
                
                elif self.door.isOpen():
                    # Exit
                    StateMethods.AcceptingBirdState.exit(self)
                    self.CURRENT_STATE = States.SCANNING
                    StateMethods.ScanningState.entry(self)

            case States.DENYING_BIRD:
                # Do
                StateMethods.DenyingBirdState.do(self)
                if isDeniedBirdDetected:
                    StateMethods.DenyingBirdState.resetTimeSinceLastDeniedBird()
                elif not isDeniedBirdDetected and StateMethods.DenyingBirdState.secondsSinceLastDeniedBird() > CLOSED_DOOR_TIMEOUT:
                    # Exit
                    StateMethods.DenyingBirdState.exit(self)
                    self.CURRENT_STATE = States.ACCEPTING_BIRD
                    StateMethods.AcceptingBirdState.entry(self)

        # This image is now processed by the statemachine and is therefore old
        latestImage = None
        isDeniedBirdDetected = None