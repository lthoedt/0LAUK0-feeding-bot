import logging
import unittest

from .Classifier import Classifier


class TestClassifier(unittest.TestCase):
    def test_connection(self):
        try:
            _classifier = Classifier()
        except Exception:
            self.fail("classifier could not connect to roboflow inference server!")

    def test_no_birds(self):
        classifier = Classifier()
        self.assertIsNone(classifier.isDeniedBird("geenvogel.jpg"))

    def test_denied_bird(self):
        classifier = Classifier()
        self.assertTrue(classifier.isDeniedBird("wateenkraai.jpg"))

    def test_good_bird(self):
        classifier = Classifier()
        self.assertFalse(classifier.isDeniedBird("wateenmus.jpg"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
