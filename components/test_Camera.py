import logging
import unittest

from Camera import Camera
from PIL.Image import Image
import time

class TestCamera(unittest.TestCase):
    def setUp(self):
        self._camera = Camera()

    def test_image_exists(self):
        self._camera.takePicture()
        time.sleep(2)
        image = self._camera.getImage()

        self.assertIsNotNone(image)
        logging.debug("Received image!")
        self.assertIsInstance(image, Image)

    def tearDown(self):
        self._camera.picamera.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
