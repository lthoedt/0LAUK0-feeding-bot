from ServoWrapper import ServoWrapper
import logging

logger = logging.getLogger(__name__)


class Door:
    openedAngle = 90
    closedAngle = 0

    def __init__(self) -> None:
        self.servo = ServoWrapper(18, 0.5)
        return

    def open(self) -> None:
        self.servo.goToAngle(openedAngle)
        return

    def isOpen(self) -> bool:
        return currentAngle == openedAngle

    def close(self) -> None:
        self.servo.goToAngle(closedAngle)
        return

    def isClosed(self) -> bool:
        return currentAngle == closedAngle
        # TODO: Implement
        return True


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
