# docker build -t sqeezenet-from-torchvision:latest .

FROM ubuntu:16.04

RUN apt-get update && apt-get install -y libopencv-dev pkg-config wget
RUN wget -c https://download.pytorch.org/models/squeezenet1_1-f364aa15.pth
COPY . ./.torch/models/