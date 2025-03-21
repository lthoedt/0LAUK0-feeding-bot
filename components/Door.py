from ServoWrapper import ServoWrapper

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