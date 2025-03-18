import logging
logger = logging.getLogger(__name__)

from States import States
import StateMethods
from components.Camera import Camera
from components.Classifier import Classifier
from components.Door import Door


class MainSystem:
    def __init__(self) -> None:
        logger.debug("Initialising main system ...")
        self.CURRENT_STATE = States.SCANNING
        self.camera = Camera()
        self.classifier = Classifier()
        self.door = Door()
        logger.debug("Finished initialising main system")

    def loop(self) -> None:
        # State machine
        # In each case the corresponding State class is called
        # The state class will have an entry, do, and exit method
        # In each case an exit check is performed to determine if the state should change
        # Upon true, the exit method is called and the state is changed to the next state and the entry method is called

        match self.CURRENT_STATE:
            case States.SCANNING:
                StateMethods.ScanningState.do(self)
                if self._deniedBirdDetected():
                    StateMethods.ScanningState.exit(self)
                    self.CURRENT_STATE = States.DENYING_BIRD
                    StateMethods.DenyingBirdState.entry(self)

            case States.ACCEPTING_BIRD:
                # Do
                StateMethods.AcceptingBirdState.do(self)
                if self.door.isOpen():
                    # Exit
                    StateMethods.AcceptingBirdState.exit(self)
                    self.CURRENT_STATE = States.SCANNING
                    StateMethods.ScanningState.entry(self)

            case States.DENYING_BIRD:
                # Do
                StateMethods.DenyingBirdState.do(self)
                if not self._deniedBirdDetected():
                    # Exit
                    StateMethods.DenyingBirdState.exit(self)
                    self.CURRENT_STATE = States.ACCEPTING_BIRD
                    StateMethods.AcceptingBirdState.entry(self)

    def _deniedBirdDetected(self):
        return self.classifier.isDeniedBird(self.camera.getImage())
