import logging
logger = logging.getLogger(__name__)


class Camera:
    def __init__(self):
        # TODO: implement
        # In this function, add any commands/logic that need to happen
        # to set up the camera and have it running
        pass

    def getImage(self):
        # TODO: implement
        # In this function, get an image from the camera and return it
        # in the form of a PIL Image, a base64 encoded in-memory file,
        # or a filepath to an image.
        # (those are the formats required for roboflow)
        # For now, it returns a reference local (static) image of a crow
        return "wateenkraai.jpg"
