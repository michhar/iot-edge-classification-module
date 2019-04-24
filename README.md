# Azure IoT Edge Classification Module

This uses a PyTorch Squeezenet model for image classification encapsulated in an Azure IoT Edge module for running on Edge Devices.

## Prerequisites

1.  Docker (Community Edition) for Mac or Windows
2.  Visual Studio Code (VSCode) text editor with IoT Edge extension (to get this go to View -> Extensions and type in "IoT Edge", select "Azure IoT Edge") - alternatively all of the work may be done on the command line as is shown in [this tutorial](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux).
3.  Azure IoT Hub resource in the Azure Cloud
4.  Azure IoT Edge Device in said Hub
5.  Set up the <a href="https://github.com/Azure/iotedgehubdev" target="_blank">IoT Edge Hub Dev Tool</a> with the Simulator (note, cannot have IoT Edge Runtime on the same machine running the Simulator)

## Instructions

### Set Up

Set up environment variables

#### MacOS

    source .set_env_unix

#### Windows (run on the command line)

    set_env_windows.sh

### Build Docker Images

Build base image

    docker build -t sqeezenet-from-torchvision:latest .

Build main image

    docker build -t <dockerhub username or anything really>/iot-edge-torchvision-module:latest .



