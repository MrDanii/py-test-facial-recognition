## Development Environment Python
FROM python:3.10.3-slim-bullseye

# Packages for linux with python distribution
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
  build-essential \
  libpq-dev \
  cmake \
  gfortran \
  git \
  wget \
  curl \
  graphicsmagick \
  libgraphicsmagick1-dev \
  libatlas-base-dev \
  libavcodec-dev \
  libavformat-dev \
  libgtk2.0-dev \
  libjpeg-dev \
  liblapack-dev \
  libswscale-dev \
  pkg-config \
  python3-dev \
  python3-numpy \
  software-properties-common \
  zip \
  && apt-get clean && rm -rf /tmp/* /var/tmp/*

#? This installs dlib, which is necessary to run face-recognition
RUN cd ~ && \
  mkdir -p dlib && \
  git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
  cd  dlib/ && \
  python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# Installing project dependencies
COPY venv/ /root/face_recognition
COPY requirements.txt /root/face_recognition
RUN cd /root/face_recognition && \
pip3 install -r requirements.txt
# pip3 install --no-cache-dir -r requirements.txt

COPY databaseconf/ /root/face_recognition/databaseconf
COPY app.py /root/face_recognition
WORKDIR /root/face_recognition

EXPOSE 5000
  # RUN cd /root/face_recognition && \
#   flask run --host=0.0.0.0 --debug

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# CMD [ "python3", "app.py"]
# flask run --host=0.0.0.0 --debug
