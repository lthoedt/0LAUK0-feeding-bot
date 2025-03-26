from ServoWrapper import ServoWrapper
import logging

from config import DOOR_CLOSED_ANGLE, DOOR_OPENED_ANGLE


logger = logging.getLogger(__name__)

class Door:
    def __init__(self) -> None:
        self.servo = ServoWrapper(12, 0.4)

    def open(self) -> None:
        logger.info("opening ...")
        self.servo.goToAngle(DOOR_OPENED_ANGLE)

    def isOpen(self) -> bool:
        isOpen = self.servo.currentAngle == DOOR_OPENED_ANGLE
        if isOpen:
            logger.info("opened")
        return isOpen

    def close(self) -> None:
        logger.info("closing ...")
        self.servo.goToAngle(DOOR_CLOSED_ANGLE)

    def isClosed(self) -> bool:
        isClosed = self.servo.currentAngle == DOOR_CLOSED_ANGLE
        if isClosed:
            logger.info("closed")
        return isClosed

class FakeDoor(Door):
    def __init__(self) -> None:
        self.state = "open"

    def open(self) -> None:
        import time

        if self.state == "closed":
            logger.info("opening ...")
            time.sleep(2)
            self.state = "open"

    def isOpen(self) -> bool:
        return self.state == "open"

    def close(self) -> None:
        import time

        if self.state == "open":
            logger.info("closing ...")
            time.sleep(2)
            self.state = "closed"

    def isClosed(self) -> bool:
        return self.state == "closed"
