FROM eclipse-temurin:8-jdk

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ysoserial-all.jar .

ENTRYPOINT ["python3", "/app/ysoserial.py"]
