from Door import Door
import logging
import time

logger = logging.getLogger(__name__)

class TestDoor:
    def __init__(self) -> None:
        self.door = Door()

    def test(self):
        self.door.open()
        time.sleep(2)
        logger.info("emergency close during opening")
        self.door.close()
        while not self.door.isClosed():
            pass
        self.door.open()
        while not self.door.isOpen():
            pass
        self.door.close()
        while not self.door.isClosed():
            pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    TestDoor().test()