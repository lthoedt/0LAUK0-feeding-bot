import logging
logger = logging.getLogger(__name__)

from config import ROBOFLOW_HOST, TIME_BETWEEN_STORED_IMAGES, STORED_IMAGE_RESOLUTION
from datetime import datetime
from inference_sdk import InferenceHTTPClient
from os import makedirs
from PIL.Image import Image
from shutil import disk_usage
from .Component import Component

class Classifier(Component):
    # A bird blacklist: list of denied bird's model classes
    # See dataset for valid class names
    deniedBirds = ["ekster", "kraai"]

    def __init__(self) -> None:
        super().__init__()
        # Initialise variables for storing images
        self._last_image_class = ""
        self._last_image_time = datetime.now()
        # Ensure the image storing directory is available
        makedirs("capturedimages", exist_ok=True)

        # Connect to the Roboflow docker client
        self.CLIENT = InferenceHTTPClient(
            # this requires the docker container to currently be running
            # this should probably be a command line option ...
            api_url=ROBOFLOW_HOST,
            # this key is from Mihai's account
            api_key="pEB4QtUJhSfoq0RI6zDp",
        )
        # Check the server connection; this function will fail (!)
        # if it cannot connect or if there are issues
        server_info = self.CLIENT.get_server_info()
        logger.info(
            f"Connected to local roboflow container (name: {server_info.name}, version: {server_info.version})"
        )

    def run(self, queueItem) -> any:
        if queueItem != None:
            return self._isDeniedBird(queueItem)
        return None        

    def scanImage(self, image) -> bool | None:
        if self.queue.empty():
            self.use(image)

    def _isDeniedBird(self, image) -> bool | None:
        # The input image must be in either of the following formats:
        # 1. PIL Image object
        # 2. base64 encoded in-memory image file (a bytes object)
        # 3. A filepath (string) to an image

        # Run the roboflow workflow
        # This workflow was configured by Mihai and uses three steps:
        # 1. object detection
        # 2. dynamically crop input image (to boundary box)
        # 3. classify bird species
        result = self.CLIENT.run_workflow(
            workspace_name="wawawa-vuk6s",  # Mihai's workspace (stupid name -- whatever)
            workflow_id="0lauk0-met-odm",
            images={
                # NOTE: It seems we can only detect one image at a time
                # with the local roboflow inference API, unless we feel like paying.
                "image": image
            },
        )
        logger.debug("Received result from roboflow: %s", result)

        if result[0]["bird_class"] == []:
            # No birds were classified with a satisfactory confidence
            # This also means no denied birds were detected
            logger.info("NO BIRD")
            return None  # This is a false-y value in Python

        # Log object detection data for debugging
        for prediction in result[0]['object_detection']['predictions']:
            logger.debug('object detected %s with conf %.2f', prediction['class'], prediction['confidence'])

        # Get the bird classes from the model prediction and store it for logging purposes
        foundBirds = [classification["top"] for classification in result[0]["bird_class"]]
        confidences = [classification["confidence"] for classification in result[0]["bird_class"]]
        if not foundBirds:
            logger.info("POSSIBLY BIRD, NOTHING CLASSIFIED")
            return None

        for idx,t in enumerate(zip(foundBirds, confidences)):
            foundBird = t[0]
            confidence = t[1]
            logger.debug("classified a bird as '%s'", foundBird)
            logger.info(
                "BIRD %d: %s\t\tCONF: %0.2f",
                idx,
                foundBird,
                confidence,
            )
            self._storeImage(image, foundBird)

        # Return true if the bird class is present in the blacklist
        return any(foundBird in Classifier.deniedBirds for foundBird in foundBirds)

    def _storeImage(self, image: Image, birdClass: str):
        """
        Stores an images of a bird that has been classified.
        Note: performs an in-place operation; do not call if image is still needed.

        Specifications:
        - Stores images at a configurable maximum frequency
        - Does not store an image if the bird has not changed since last time
        - Does not store an image if we have less than 1G free
        - Stores images in a configurable resolution (should be small, 128x128 or 320x320)
        """

        # Check if enough time has passed
        time_diff = datetime.now() - self._last_image_time
        if time_diff.total_seconds() <= TIME_BETWEEN_STORED_IMAGES:
            return
        # Check if there is enough disk space
        if disk_usage("capturedimages").free <= 1_000_000_000:  # 1 GB
            return
        # Check if the class has changed
        if birdClass == self._last_image_class:
            return
        # Checks passed -- store image
        self._last_image_class = birdClass
        self._last_image_time = datetime.now()

        # Scale (stretch) image. Note: in-place operation (we don't need the image anymore)
        image.thumbnail(size=STORED_IMAGE_RESOLUTION)
        name = f"capturedimages/{self._last_image_time.isoformat()}-{birdClass}.jpg"
        logger.debug("stored image under %s", name)

        image.save(name)
