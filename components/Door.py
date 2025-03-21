import logging

logger = logging.getLogger(__name__)


class Door:
    def __init__(self) -> None:
        return

    def open(self) -> None:
        # TODO: Implement
        return

    def isOpen(self) -> bool:
        # TODO: Implement
        return True

    def close(self) -> None:
        # TODO: Implement
        return

    def isClosed(self) -> bool:
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
