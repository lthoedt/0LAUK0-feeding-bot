from .States import States
from .StateMethods import ScanningState
from .StateMethods import AcceptingBirdState
from .StateMethods import DenyingBirdState
from .components.Door import Door

class MainSystem:
    def __init__(self) -> None:
        self.CURRENT_STATE = States.SCANNING
        self.door = Door()
        self.scanner = Scanner()
        return

    def loop(self) -> None:
        # State machine
        # In each case the corresponding State class is called
        # The state class will have an entry, do, and exit method
        # In each case an exit check is performed to determine if the state should change
        # Upon true, the exit method is called and the state is changed to the next state and the entry method is called
        match self.CURRENT_STATE:
            case States.SCANNING:
                # Do
                ScanningState.do(self)
                if (self.deniedBirdDetected()):
                    # Exit
                    ScanningState.exit(self)
                    self.CURRENT_STATE = States.DENYING_BIRD
                    DenyingBirdState.entry(self)
                break
            case States.ACCEPTING_BIRD:
                # Do
                AcceptingBirdState.do(self)
                if (self.door.isOpen()):
                    # Exit
                    AcceptingBirdState.exit(self)
                    self.CURRENT_STATE = States.SCANNING
                    ScanningState.entry(self)
                break
            case States.DENYING_BIRD:
                # Do
                DenyingBirdState.do(self)
                if (self.deniedBirdDetected() != True):
                    # Exit
                    DenyingBirdState.exit(self)
                    self.CURRENT_STATE = States.ACCEPTING_BIRD
                    AcceptingBirdState.entry(self)
                break