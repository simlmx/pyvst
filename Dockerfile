FROM ubuntu:16.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y -q \
        python3 \
        python3-pip \
        libx11-dev \
        libxext-dev \
        libxinerama-dev \
        libasound-dev \
        libfreetype6 \
        # For TyrellN6
        libglib2.0 \
        libcairo2 \
        # amsynth
        libgtk2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workdir/pyvst

COPY setup.py /workdir/pyvst/setup.py

RUN pip3 install -U pip
# Installing with -e, effectively only writing a simlink, assuming the code will be mounted.
RUN pip3 install -e /workdir/pyvst[dev]
# Putting this one here because not really a dependency
RUN pip3 install ipython

ENV HOME /workdir/pyvst
