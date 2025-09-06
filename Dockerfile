FROM python:3.10-slim-bookworm 

WORKDIR /app
COPY . /app

ARG DEBIAN_FRONTEND=noninteractive
RUN set -eux; \
    apt-get update -y; \
    apt-get install -y --no-install-recommends curl unzip ca-certificates; \
    curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip; \
    unzip awscliv2.zip; \
    ./aws/install; \
    rm -rf /var/lib/apt/lists/* awscliv2.zip aws

# Do NOT run apt-get update again if you’re not installing apt packages
RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
