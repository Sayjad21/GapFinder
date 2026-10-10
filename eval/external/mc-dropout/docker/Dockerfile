# MC Dropout (Gal & Ghahramani, ICML 2016) artifact, pinned to the README's Theano/Keras era.
# Build from eval/external/mc-dropout/ (the context needs harness/run_cell.sh):
#   docker build -t gf-mcdropout -f docker/Dockerfile .
# The only change to the artifact is the documented Monte Carlo sample patch (T = 10000 -> 100).
FROM python:3.6-slim

# python:3.6-slim is Debian 11 (bullseye), whose package mirrors have moved to the archive.
RUN sed -i -e 's|deb.debian.org|archive.debian.org|g' -e 's|security.debian.org|archive.debian.org|g' \
        -e '/bullseye-updates/d' /etc/apt/sources.list 2>/dev/null || true; \
    for f in /etc/apt/sources.list.d/*; do [ -f "$f" ] && sed -i -e 's|deb.debian.org|archive.debian.org|g' -e 's|security.debian.org|archive.debian.org|g' -e '/bullseye-updates/d' "$f"; done; \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99archive \
 && apt-get update \
 && apt-get install -y --no-install-recommends g++ git ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    numpy==1.13.3 scipy==1.1.0 h5py==2.8.0 Theano==0.8.2 Keras==2.2.0

ENV THEANO_FLAGS='device=cpu,floatX=float32' \
    KERAS_BACKEND=theano

# Current master of yaringal/DropoutUncertaintyExps when this image was defined.
ARG REPO_COMMIT=6eb4497628d12b0f300f4b4f6bdc386bebad565c
RUN git clone https://github.com/yaringal/DropoutUncertaintyExps /work \
 && cd /work && git checkout ${REPO_COMMIT} \
 && sed -i 's/T = 10000/T = 100/' net/net.py \
 && grep -n 'T = 100' net/net.py

WORKDIR /work
COPY harness/run_cell.sh /work/run_cell.sh
