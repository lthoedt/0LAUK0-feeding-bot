import logging
logger = logging.getLogger(__name__)

try:  # This shitty try-except block makes this thing 'run' on PC
    from picamera2 import Picamera2
except:
    pass
from time import sleep

from Component import Component

class Camera(Component):
    isCapturing = False
    def __init__(self):
        super().__init__()
        # TODO: implement
        # In this function, add any commands/logic that need to happen
        # to set up the camera and have it running
        logger.debug("Starting camera ...")
        self.picamera = Picamera2()
        self.picamera.start()

        self.setImage(None)
        sleep(1)  # We wait a little to ensure the camera is actually started

    # This method returns the latest image taken by the camera
    # Once the image is read it is removed this prevents the same image being read multiple times
    def getImage(self):
        image = self._image
        self._image = None
        return image
    
    def setImage(self, image):
        self._image = image

    def run(self, queueItem) -> bool:
        if self.isCapturing:
            return False

        if queueItem != None:
            self.isCapturing = True
            self._takePicture()
            self.isCapturing = False

        return True
    
    # This method actually take the picture
    def _takePicture(self):
        # In this function, get an image from the camera and return it
        # in the form of a PIL Image, a base64 encoded in-memory file,
        # or a filepath to an image.
        # (those are the formats required for roboflow)

        # This command is blocking
        logger.debug("Capturing image ...")
        self.setImage(self.picamera.capture_image("main"))

    # This method makes a request to take a picture, can be called multiple times which wont result in multiple pictures being taken
    def takePicture(self):
        # Prevents another capture request if one is already going on
        if self.queue.empty():
            self.use("capture")

class FakeCamera(Camera):
    def __init__(self):
        super().__init__()
        pass

    def _takePicture(self):
        from random import choice
        import PIL

        random_image = choice(["geenvogel.jpg", "wateenkraai.jpg", "wateenmus.jpg"])
        logger.debug("Random image sent %s", random_image)
        self.setImage(PIL.Image.open(random_image))
