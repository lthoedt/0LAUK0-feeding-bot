import logging
logger = logging.getLogger(__name__)

from inference_sdk import InferenceHTTPClient

class Classifier:
    # A bird blacklist: list of denied bird's model classes
    # See dataset for valid class names
    deniedBirds = [ 'ekster', 'kraai' ]

    def __init__(self) -> None:
        # Connect to the Roboflow docker client
        self.CLIENT = InferenceHTTPClient(
            # this requires the docker container to currently be running
            api_url="http://localhost:9001",    
            # this key is from Mihai's account
            api_key="pEB4QtUJhSfoq0RI6zDp"
        )
        # Check the server connection; this function will fail (!)
        # if it cannot connect or if there are issues
        server_info = self.CLIENT.get_server_info()
        logger.info(f'Connected to local roboflow container (name: {server_info.name}, version: {server_info.version})')

    def isDeniedBird(self, image) -> bool | None:
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
            workspace_name="wawawa-vuk6s",    # Mihai's workspace (stupid name -- whatever)
            workflow_id="0lauk0-met-odm",
            images={
                # NOTE: It seems we can only detect one image at a time
                # with the local roboflow inference API, unless we feel like paying. 
                "image": image
            }
        )
        logger.debug('Received result from roboflow: %s', result)

        if result[0]["bird_class"] == []:
            # No birds were classified with a satisfactory confidence
            # This also means no denied birds were detected
            return None    # This is a false-y value in Python

        # Get the bird class from the model prediction and store it for logging purposes
        foundBird = result[0]["bird_class"][0]["top"]
        logger.debug('classified a bird as \'%s\'', foundBird)
        self._storeImage(image, foundBird)

        # Return true if the bird class is present in the blacklist
        return foundBird in Classifier.deniedBirds

    def _storeImage(self, image, birdClass):
        # TODO: implement
        logger.debug('method not yet implemented')
        pass
