import torch
import torchvision.models as models
import sys
import os
import json


sys.path.append(os.getcwd())

# If there's CUDA, use it!
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Classifier(object):

    def __init__(self):
        """Initialize classifier by loading the model and
        classes"""
        self.model = models.squeezenet1_0(pretrained=True)
        with open('imagenet_class_index.json', 'r') as f:
            self.classes = json.load(f)

    def classify(self, image):
        """Perform the classification with the torchvision
        model - image must be in the right shape and transformed
        appropriately"""
        result = {}
        with torch.no_grad():
            output = self.model(image)
            _, pred = torch.max(output, 1)
            result = {'prediction': self.classes[str(pred.item())]}
        return result
