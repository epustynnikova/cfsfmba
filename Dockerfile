FROM ubuntu:20.04
MAINTAINER Elena Pustynnikova <elena.pustynnikova.work@gmail.com>

ARG SAMTOOLSVER=1.14
ARG SOFT_PATH="soft/"

#LABEL description="Tools (written in C using htslib) for manipulating next-generation sequencing data"

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update

RUN apt-get install -y \
    liblzma-dev \
    python3-biopython \
    python3-dev \
    python3-matplotlib \
    python3-numpy \
    python3-pip \
    python3-reportlab \
    python3-scipy \
    python3-tk \
    zlib1g-dev \
    wget \
    gcc \
    wget \
    make \
    bzip2 \
    libbz2-dev \
    && apt-get autoclean && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U Cython
RUN pip3 install -U future futures pandas pomegranate pyfaidx

# install samtools, make /data
#RUN wget https://github.com/samtools/samtools/releases/download/${SAMTOOLSVER}/samtools-${SAMTOOLSVER}.tar.bz2 && \
# tar -xjf samtools-${SAMTOOLSVER}.tar.bz2 && \
# rm samtools-${SAMTOOLSVER}.tar.bz2 && \
# cd samtools-${SAMTOOLSVER} && \
# ./configure && \
# make && \
# make install

## USER CONFIGURATION, containers should not run as root
RUN adduser --disabled-password --gecos '' ubuntu && chsh -s /bin/bash && mkdir -p /home/ubuntu
USER    ubuntu
WORKDIR /home/ubuntu

CMD ["bash"]
