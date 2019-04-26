"""
Largely based on https://github.com/vjrantal/iot-edge-darknet-module/blob/master/module.py
"""
import os
import cv2
import json
import time
from PIL import Image
from torchvision import transforms
import torch
from sender import Sender
from classifier import Classifier


# If there's CUDA, use it!
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Can be used to change used camera in case multiple available
CAMERA_INDEX = int(os.getenv('OPENCV_CAMERA_INDEX', 0))

# Can be used for testing purposes to limit the amount of detections
# performed (0 means loop forever)
CLASSIFICATION_COUNT = int(os.getenv('CLASSIFICATION_COUNT', 0))

# This environment variable is set when the module is started by the
# IoT Edge runtime
IS_EDGE = os.getenv('IOTEDGE_MODULEID', False)

if IS_EDGE:
    sender = Sender()
else:
    sender = False

video_capture = cv2.VideoCapture(CAMERA_INDEX)
classifier = Classifier()

# Prepare image for inference
loader = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def transform_image(array):
    """Transform a numpy array into a torch tensor, 
    resized and normalized correctly - most torchvision
    transforms operate on PIL Image format"""
    # Converts to a PIL Image
    image = Image.fromarray(np.uint8(array))
    # Creates a torch tensor
    image = loader(pil_image).float()
    return image.to(device)

# Keep count of classifcations performed
classification_index = 0

while True:
    
    capture = video_capture.read()
    if capture[0]:
        array = capture[1]
        type = 'captured'
    else:
        type = 'static'
        array = cv2.imread(os.join.path('sample_data', 'bear.jpg'))
    image = transform_image(array)

    time_before = time.time()
    result = classifier.classify(image)
    time_after = time.time()
    print('Classification took %s seconds' % (time_after - time_before))
    print(json.dumps(result, indent=4))
    classification_index += 1

    if sender:
        msg_properties = {
            'classification_index': str(classification_index)
        }
        json_formatted = json.dumps(result)
        sender.send_event_to_output('classificationOutput', json_formatted, msg_properties, classification_index)

    if CLASSIFICATION_COUNT > 0 and classification_index >= CLASSIFICATION_COUNT:
        break

    # To avoid sending too frequently on hardware where detection is fast
    time.sleep(1)

# This stdout print is currently checked in the Travis CI script exactly
# as it is so pay attention if changing it
print('Program exiting normally')