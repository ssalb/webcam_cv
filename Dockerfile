FROM ubuntu:16.04

ENV API_PORT 5000

COPY . /app

WORKDIR /app
RUN mkdir logs

RUN apt-get update -y

RUN apt-get install -y \
	 build-essential cmake unzip pkg-config \
	 libjpeg-dev libpng-dev libtiff-dev libavcodec-dev \
	 libavformat-dev libswscale-dev libv4l-dev \
	 libxvidcore-dev libx264-dev libgtk-3-dev \
	 libatlas-base-dev gfortran python3 python3-dev python3-pip

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "-c", "gunicorn.py", "app:app"]
