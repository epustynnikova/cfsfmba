FROM ubuntu:20.04
MAINTAINER Elena Pustynnikova <elena.pustynnikova.work@gmail.com>

ARG SAMTOOLSVER=1.14
WORKDIR /soft

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
    libncurses-dev \
    libgsl-dev \
    libperl-dev \
    && apt-get autoclean && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U Cython
RUN pip3 install -U future futures pandas pomegranate pyfaidx pysam deflate

# install samtools, bcftools, make /data
RUN wget https://github.com/samtools/htslib/releases/download/${SAMTOOLSVER}/htslib-${SAMTOOLSVER}.tar.bz2 && \
 tar -xjf htslib-${SAMTOOLSVER}.tar.bz2 && \
 rm htslib-${SAMTOOLSVER}.tar.bz2 && \
 cd htslib-${SAMTOOLSVER} && \
 ./configure --enable-plugins --with-plugin-path='$(libexecdir)/htslib:/usr/libexec/htslib' && \
 make && \
 make install

RUN wget https://github.com/samtools/samtools/releases/download/${SAMTOOLSVER}/samtools-${SAMTOOLSVER}.tar.bz2 && \
 tar -xjf samtools-${SAMTOOLSVER}.tar.bz2 && \
 rm samtools-${SAMTOOLSVER}.tar.bz2 && \
 cd samtools-${SAMTOOLSVER} && \
 ./configure --with-htslib=system  && \
 make && \
 make install

RUN wget https://github.com/samtools/bcftools/releases/download/${SAMTOOLSVER}/bcftools-${SAMTOOLSVER}.tar.bz2 && \
 tar -xjf bcftools-${SAMTOOLSVER}.tar.bz2 && \
 rm bcftools-${SAMTOOLSVER}.tar.bz2 && \
 cd bcftools-${SAMTOOLSVER} && \
 ./configure --enable-libgsl --enable-perl-filters --with-htslib=system  && \
 make && \
 make install

## USER CONFIGURATION, containers should not run as root
RUN adduser --disabled-password --gecos '' docker_user && chsh -s /bin/bash && mkdir -p /home/docker_user
USER    docker_user
WORKDIR /home/docker_user

WORKDIR /home/docker_user
COPY scripts/transform.py ./
COPY data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv ./

RUN cd ../
CMD ["bash"]
