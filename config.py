import os

cwd = os.getcwd()

# Object detection model
ODM_WEIGHTS = "{}/yolo_v3/yolov3.weights".format(cwd)
ODM_CONFIG = "{}/yolo_v3/yolov3.cfg".format(cwd)
ODM_CLASSES = "{}/yolo_v3/yolov3.names".format(cwd)

# Faces data_path
FACES_PATH = "{}/local_data".format(cwd)
