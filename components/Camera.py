import logging
logger = logging.getLogger(__name__)

try:  # This shitty try-except block makes this thing 'run' on PC
    from picamera2 import Picamera2
except:
    pass
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


class FakeCamera(Camera):
    def __init__(self):
        pass

    def getImage(self):
        from random import choice
        import PIL

        random_image = choice(["geenvogel.jpg", "wateenkraai.jpg", "wateenmus.jpg"])
        logger.debug("Random image sent %s", random_image)
        return PIL.Image.open(random_image)
