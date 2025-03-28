DRY_RUN = False
# minimum time interval (in seconds) per tick
# use this variable to prevent busy waiting
ROBOT_MINIMUM_SPT = 0.5

# ROBOFLOW_HOST = "http://localhost:9001"
ROBOFLOW_HOST = "http://192.168.137.72:9001"


# Minimum time between two stored images in seconds
TIME_BETWEEN_STORED_IMAGES = 1.0
# Resolution of stored images
STORED_IMAGE_RESOLUTION = (128, 128)

CLOSED_DOOR_TIMEOUT = 20

DOOR_OPENED_ANGLE = 90
DOOR_CLOSED_ANGLE = 0