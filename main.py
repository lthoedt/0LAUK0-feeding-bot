from MainSystem import MainSystem

class Robot:
    def __init__(self) -> None:
        self.system = MainSystem()

    def loop(self):
        self.system.loop()

if __name__ == '__main__':
    robot = Robot()
    while True:
        robot.loop()