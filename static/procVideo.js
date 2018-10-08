//Parameters
const s = document.getElementById('procVideo');
const sourceVideo = s.getAttribute("data-source");  //the source video to use
const mirror = s.getAttribute("data-mirror") || false; //mirror the boundary boxes
const scoreThreshold = s.getAttribute("data-scoreThreshold") || 0.5;
const apiServer = window.location.origin + s.getAttribute("data-apiServer") ||
                  window.location.origin + '/api/obj_detect';

console.log(apiServer);
var video = document.getElementById(sourceVideo);

//for starting events
let isPlaying = false,
    gotMetadata = false;

//Canvas setup

//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext("2d");

//create a canvas for drawing object boundaries
let drawCanvas = document.getElementById('drCanvas');
// document.body.appendChild(drawCanvas);
let drawCtx = drawCanvas.getContext("2d");

//draw boxes and labels on each detected object
function drawBoxes(objects) {

    //clear the previous drawings
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);

    //filter out objects that contain a class_name and then draw boxes and labels on each
    objects.filter(object => object.name).forEach(object => {
        let x = object.x*drawCtx.canvas.width;
        let y = object.y*drawCtx.canvas.height;
        let width = object.width*drawCtx.canvas.width;
        let height = object.height*drawCtx.canvas.height;
        //flip the x axis if local video is mirrored
        if (mirror) {
            x = drawCtx.canvas.width - (x + width)
        }

        if (!!object.score) {
          drawCtx.fillText(object.name + " - " + Math.round(object.score * 100) + "%",
                            x + 5, y + 20);
        } else {
          drawCtx.fillText(object.name, x + 5, y + 20);
        }
        drawCtx.strokeRect(x, y, width, height);

    });
}

//Add file blob to a form and post
function postFile(file) {

    //Set options as form data
    let formdata = new FormData();
    formdata.append("image", file);
    formdata.append("threshold", scoreThreshold);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', apiServer, true);
    xhr.onload = function () {
        if (this.status === 200) {
            let resp = JSON.parse(this.response);
            if (resp.status === "success") {
              drawBoxes(resp.payload);
            }
            imageCtx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0,
                                video.videoWidth, video.videoHeight);
            imageCanvas.toBlob(postFile, 'image/jpeg');
        }
        else {
            console.error(xhr);
        }
    };
    xhr.send(formdata);
}

function startObjectDetection() {

    console.log("starting object detection");

    drawCtx.canvas.width = video.videoWidth;
    drawCtx.canvas.height = video.videoHeight;

    imageCtx.canvas.width = video.videoWidth;
    imageCtx.canvas.height = video.videoHeight;

    drawCtx.lineWidth = 2;
    drawCtx.strokeStyle = "#0066ff";
    drawCtx.font = "18px Verdana";
    drawCtx.fillStyle = "#0066ff";

    //Save and send the first image
    imageCtx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0,
                        video.videoWidth, video.videoHeight);
    imageCanvas.toBlob(postFile, 'image/jpeg');

}

//Starting events

//check if metadata is ready - we need the video size
video.onloadedmetadata = () => {
    console.log("video metadata ready");
    gotMetadata = true;
    if (isPlaying)
        startObjectDetection();
};

//see if the video has started playing
video.onplaying = () => {
    console.log("video playing");
    isPlaying = true;
    if (gotMetadata) {
        startObjectDetection();
    }
};
