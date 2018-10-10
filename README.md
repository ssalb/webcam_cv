# Webcam CV - computer vision demo in the browser

This is a (Dockerised) demo for object detection and face recognition tasks in the browser. A [Flask](http://flask.pocoo.org/) app serves some very simple pages and a JavaScript script, which takes snapshots from the camera stream and sends them back through a POST request. Then, the images are processed using [OpenCV](https://opencv.org/) and [face_recognition](https://github.com/ageitgey/face_recognition) in python; bounding boxes, labels and scores are sent back in the request's response.

**Important**: This demo uses `HTML5` to handle the camera, thus you'll need a browser that supports it.

## Prepare everything

First, of course, clone this repo ;).

For the object detection part, you'll need to download the Yolov3 model. To this end, go to https://github.com/pjreddie/darknet/ and download  `data/coco.names` (rename it as `yolov3.names`) and `cfg/yolov3.cfg`. Also, download the pre-trained model weights from https://pjreddie.com/media/files/yolov3.weights. Save these 3 files under `yolo_v3/`. Alternatively, you could get these files using wget within the Dockerfile, if you don't mind downloading them every time you build the image.

For the face recognition part, put your face images under `/local_data` in `jpg` format with the name you want displayed as the image name. For example `Alice.jpg` and `Bob.jpg` would be the images of Alice's and Bob's faces, respectively.

## Run the app

To run it using Docker simply run
```
docker build -t webcam_cv .
```
inside the repo's directory to build the image (wait for a little while - maybe have a coffee), and then run
```
docker run -p 5000:5000 -v $(pwd):/app --name webcam_cv webcam_cv
```
if you're running it for the first time (add `-d` to run it detached from your shell). It will be available under http://localhost:5000 using the repo's directory as a shared volume. Later you can start/stop it by running
```
docker start/stop webcam_cv
```

You could also run it without Docker, but then you'll need to handle dependencies by yourself.

## Note

To run this on a server (i.e. other than `localhost`), you'll need to configure it to run over https, otherwise you won't have access to the camera - after all, you don't want your video stream to be sent unencrypted over the internet, do you?. How to do that is out of the scope of this document, but in case it's useful for you, I've successfully done this for a demo using a AWS EC2 instance, a free domain name, and [Certbot](https://certbot.eff.org/). You'll have to either change the `gunicorn.py` config file or set up another web server, like apache or nginx (that's what I used).

## Credits

As most of what we do (or human knowledge in general), this is based on others work.

HTML and JS scripts to handle the camera stream are based on:
https://github.com/webrtcHacks/tfObjWebrtc

To know more about Yolo v3, go to:
https://pjreddie.com
and/or
https://www.learnopencv.com/deep-learning-based-object-detection-using-yolov3-with-opencv-python-c/

Last but not least, the `face_recognition` github repo can be found here:
https://github.com/ageitgey/face_recognition
