import torchvision.models as models
from torchvision import datasets, transforms
import torch.nn as nn
import torch
import numpy as np
from PIL import Image
import os
import json


# If there's CUDA, use it!
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Read in ImageNet classes from file
with open(os.path.join('..', 'imagenet_class_index.json'), 'r') as f:
    imagenet_classes = json.load(f)

# Transform input images to work with model
data_transforms = {
    'bear': transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
}

# Deal with data
data_dir = os.path.join(os.getcwd(), '..', 'data')

# Create a dataset that wraps around a folder of images
image_dataset = datasets.ImageFolder(data_dir,
                                          data_transforms['bear'])

# Create a loader that loads one image at a time from the dataset
dataloader = torch.utils.data.DataLoader(image_dataset, batch_size=1,
                                             shuffle=False, num_workers=0)

def get_model():
    """Download and/or load the model"""
    # This will check for model at ~/.torch/models and if not there will download
    # This model was trained on ImageNet
    model = models.squeezenet1_0(pretrained=True)
    print(model.classifier._modules)
    # Could change last layer to change number of output classes and load a custom
    # model with squeezenet architecture (e.g. Bears)
    # model.classifier._modules['6'] = nn.Linear(4096, 2)
    return model

def test_model(model):
    """Perform inference on a test image"""
    for i, (inputs, labels) in enumerate(dataloader):
        img = inputs.to(device)
        with torch.no_grad():
            output = model(img)
            _, pred = torch.max(output, 1)
            print(imagenet_classes[str(pred.item())])

def main():
    model = get_model()
    test_model(model)

if __name__ == "__main__":
    main()
