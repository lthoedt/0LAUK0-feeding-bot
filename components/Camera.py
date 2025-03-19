import logging
logger = logging.getLogger(__name__)

from picamera2 import Picamera2
from time import sleep


class Camera:
    def __init__(self):
        # TODO: implement
        # In this function, add any commands/logic that need to happen
        # to set up the camera and have it running
        logger.debug("Starting camera ...")
        self.picamera = Picamera2()
        self.picamera.start()
        sleep(1)  # We wait a little to ensure the camera is actually started

    def getImage(self):
        # In this function, get an image from the camera and return it
        # in the form of a PIL Image, a base64 encoded in-memory file,
        # or a filepath to an image.
        # (those are the formats required for roboflow)

        # This command is blocking
        logger.debug("Capturing image ...")
        return self.picamera.capture_image("main")
