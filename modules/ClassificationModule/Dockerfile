FROM rheartpython/sqeezenet-from-torchvision:latest

WORKDIR /

RUN apt-get update && \
    apt-get install -y --no-install-recommends libcurl4-openssl-dev \
    python3-pip \
    libboost-python1.58-dev \
    libpython3-dev \
    python-opencv && \
    rm -rf /var/lib/apt/lists/* 

RUN pip3 install --upgrade pip
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash moduleuser
USER moduleuser

CMD ["python3", "-u", "module.py"]


