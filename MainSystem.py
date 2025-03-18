import logging
logger = logging.getLogger(__name__)

from States import States
import StateMethods
from components.Door import Door
from components.Scanner import Scanner

class MainSystem:
    def __init__(self) -> None:
        logger.debug('Initialising main system ...')
        self.CURRENT_STATE = States.SCANNING
        self.door = Door()
        self.scanner = Scanner()


    def loop(self) -> None:
        # State machine
        # In each case the corresponding State class is called
        # The state class will have an entry, do, and exit method
        # In each case an exit check is performed to determine if the state should change
        # Upon true, the exit method is called and the state is changed to the next state and the entry method is called

        match self.CURRENT_STATE:
            case States.SCANNING:
                StateMethods.ScanningState.do(self)
                if (self.scanner.deniedBirdDetected()):
                    StateMethods.ScanningState.exit(self)
                    self.CURRENT_STATE = States.DENYING_BIRD
                    StateMethods.DenyingBirdState.entry(self)

            case States.ACCEPTING_BIRD:
                # Do
                StateMethods.AcceptingBirdState.do(self)
                if (self.door.isOpen()):
                    # Exit
                    StateMethods.AcceptingBirdState.exit(self)
                    self.CURRENT_STATE = States.SCANNING
                    StateMethods.ScanningState.entry(self)

            case States.DENYING_BIRD:
                # Do
                StateMethods.DenyingBirdState.do(self)
                if (self.scanner.deniedBirdDetected() != True):
                    # Exit
                    StateMethods.DenyingBirdState.exit(self)
                    self.CURRENT_STATE = States.ACCEPTING_BIRD
                    StateMethods.AcceptingBirdState.entry(self)
