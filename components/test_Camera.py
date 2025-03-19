import logging
import unittest

from Camera import Camera
from PIL.Image import Image


class TestCamera(unittest.TestCase):
    def setUp(self):
        self._camera = Camera()

    def test_image_exists(self):
        image = self._camera.getImage()
        logging.debug("Received image!")
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)

    def tearDown(self):
        self._camera.picamera.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
