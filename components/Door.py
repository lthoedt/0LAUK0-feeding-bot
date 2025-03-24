from ServoWrapper import ServoWrapper
import logging

logger = logging.getLogger(__name__)


class Door:
    openedAngle = 90
    closedAngle = 0

    def __init__(self) -> None:
        self.servo = ServoWrapper(12, 0.4)

    def open(self) -> None:
        logger.info("opening ...")
        self.servo.goToAngle(self.openedAngle)

    def isOpen(self) -> bool:
        isOpen = self.servo.currentAngle == self.openedAngle
        if isOpen:
            logger.info("open")
        return isOpen

    def close(self) -> None:
        logger.info("closing ...")
        self.servo.goToAngle(self.closedAngle)

    def isClosed(self) -> bool:
        isClosed = self.servo.currentAngle == self.closedAngle
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
