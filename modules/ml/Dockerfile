# Base Image
FROM python:3.8

# Set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Set project environment variables
# Grab these via Python's os.environ
# These are 100% optional here
ENV PYTHONPATH "${PYTHONPATH}:/var/app"
ENV LOCAL_DB_URI=sqlite:////artifacts/local.db
ENV CAND_PATH=/artifacts/cand.bin
ENV RTRV_PATH=/artifacts/rtrv.bin
ENV LOCAL_IDX_PATH=/artifacts/local_index.bin
ENV REMOTE_IDX_PATH=/artifacts/remote_index.bin

# Create and set working directory
RUN mkdir -p /var/app/modules/ml

# Add current directory code to working directory
COPY modules/ml/data/ /var/app/modules/ml/data
COPY modules/ml/document_store/ /var/app/modules/ml/document_store
COPY modules/ml/plugins/ /var/app/modules/ml/plugins
COPY modules/ml/preprocessor/ /var/app/modules/ml/preprocessor
COPY modules/ml/retriever/ /var/app/modules/ml/retriever
COPY modules/ml/vectorizer/ /var/app/modules/ml/vectorizer
COPY modules/ml/*.py /var/app/modules/ml/
COPY requirements.txt /var/app/modules/ml/requirements.txt

# Install system dependencies
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends \
    tzdata \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    curl \
    && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install environment dependencies
RUN pip3 install --upgrade pip

# Install project dependencies
WORKDIR /var/app/modules/ml
RUN pip3 install -r requirements.txt

# Run the Python task
WORKDIR /var/app
CMD ["python", "modules/ml/cronjobs.py"]
