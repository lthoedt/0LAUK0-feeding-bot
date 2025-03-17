import logging

from Scanner import Scanner

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    scanner = Scanner()

    # NOTE: This example uses a static image, but it can also contain an image filepath or a PIL Image object
    scanner.deniedBirdDetected("/home/m/Study/0lauk0/0LAUK0-feeding-bot/wateenkraai.jpg")
