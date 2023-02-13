FROM python:3.8.15-buster

RUN apt update && \
    apt install -y --no-install-recommends \
    curl \
    tini && \
    apt clean &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN python3 -m pip install --no-cache-dir --progress-bar off -U pip setuptools wheel && \
    python3 -m pip install --no-cache-dir --progress-bar off -e .

ENTRYPOINT ["tini", "--"]
CMD ["sleep", "infinity"]