
FROM python:2-slim
LABEL maintainer "SvenDowideit@home.org.au"
LABEL name "pi-frame"
LABEL version "0.0.1"

RUN apt-get update && apt-get install -y fbi --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
COPY . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 5555
ENTRYPOINT ["python"]
CMD ["runserver.py"]
