# blind-2: GraphMAE (Hou et al., KDD 2022) at the sealed commit, for local Docker runs (HARNESS.md).
# Build from eval/external/blind-2/ (the context needs harness/):
#   docker build -t gf-graphmae -f docker/Dockerfile .
# Why not Sandboxes: COLLAB, the target, needs more than the VM's 3.9 GB to load (OOM-killed at 3.9 GB RSS,
# and a VM can't add swap), so the runs use this machine's memory. Same pins as the Sandboxes image.
# No change to the artifact.
FROM python:3.10-slim

RUN pip install --no-cache-dir 'torch==1.13.1+cpu' --extra-index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir 'dgl==0.9.1' 'numpy<2' 'scipy<1.12' 'scikit-learn<1.4' 'pyyaml==6.0.1' tqdm tensorboardX ogb

ARG REPO_COMMIT=1be594160bb7c1fde0d16ced6af1e88b53612e49
RUN python -c "import io, tarfile, urllib.request; d = urllib.request.urlopen('https://codeload.github.com/THUDM/GraphMAE/tar.gz/${REPO_COMMIT}', timeout=300).read(); tarfile.open(fileobj=io.BytesIO(d)).extractall('/tmp/src')" \
 && mkdir -p /work && cp -r /tmp/src/GraphMAE-${REPO_COMMIT}/. /work/ && rm -rf /tmp/src

# the Table 2 datasets, fetched once at build time so runs need no network (DGL's TUDataset cache, ~/.dgl)
RUN python -c "from dgl.data import TUDataset; [print(n, len(TUDataset(n))) for n in ['COLLAB', 'IMDB-BINARY', 'IMDB-MULTI', 'PROTEINS', 'MUTAG']]"

WORKDIR /work
COPY harness/ /work/gf_harness/
