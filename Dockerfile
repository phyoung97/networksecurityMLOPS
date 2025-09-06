FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y \
 && apt-get install -y --no-install-recommends curl unzip ca-certificates \
 && curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip \
 && unzip awscliv2.zip \
 && ./aws/install \
 && rm -rf /var/lib/apt/lists/* awscliv2.zip aws

RUN apt-get update && pip install -r requirements.txt
CMD ["python3", "app.py"]