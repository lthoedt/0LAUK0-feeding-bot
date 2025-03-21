from Door import Door

class TestDoor:
    def __init__(self) -> None:
        self.door = Door()

    def test(self):
        isClosing = False
        while True:
            if (isClosing):
                self.door.close()
                if (self.door.isClosed()):
                    isClosing = False
            else:
                self.door.open()
                if (self.door.isOpen()):
                    isClosing = True

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    TestDoor().test()