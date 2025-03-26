import logging
import unittest

from Classifier import Classifier

from time import sleep

class TestClassifier(unittest.TestCase):
    def test_connection(self):
        try:
            _classifier = Classifier()
        except Exception:
            self.fail("classifier could not connect to roboflow inference server!")

    def test_no_birds(self):
        classifier = Classifier()
        classifier.scanImage("geenvogel.jpg")
        sleep(5)
        self.assertIsNone(classifier.getResult())

    def test_denied_bird(self):
        classifier = Classifier()
        classifier.scanImage("wateenkraai.jpg")
        sleep(5)
        self.assertTrue(classifier.getResult())

    def test_good_bird(self):
        classifier = Classifier()
        classifier.scanImage("wateenmus.jpg")
        sleep(5)
        self.assertFalse(classifier.getResult())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
