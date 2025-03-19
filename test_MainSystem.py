import logging
import unittest

from MainSystem import MainSystem


class TestCamera(unittest.TestCase):
    def setUp(self):
        self._main_system = MainSystem()

    def test_recognize_image(self):
        """
        This is not an automated test.
        Read the logs to confirm if this works.
        """
        self._main_system._deniedBirdDetected()

    def tearDown(self):
        self._main_system.camera.picamera.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
