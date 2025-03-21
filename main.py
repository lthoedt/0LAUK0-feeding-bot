import logging

from config import ROBOT_MINIMUM_SPT
from MainSystem import MainSystem
from time import sleep


class Robot:
    def __init__(self) -> None:
        self.system = MainSystem()

    def loop(self):
        self.system.loop()
        # This sleep intentionally slows down the system.
        # We currently (and might never) have code in place to do lazy waiting,
        # so we need to intentionally sleep our infinite loops in order to not
        # use 100% on busy waits and heat our RPi unnecessarily.
        sleep(ROBOT_MINIMUM_SPT)  # 50ms <==> ~20 Hz


if __name__ == "__main__":
    # DEBUG output and above gets written to stdout
    logging.basicConfig(level=logging.INFO)

    robot = Robot()
    while True:
        robot.loop()
