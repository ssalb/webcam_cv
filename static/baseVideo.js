var video = document.getElementById("videoElement");

// window.AudioContext = window.AudioContext || window.webkitAudioContext;
// const audioContext = new AudioContext();

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({
      // audio: true,
      video: true
    })
  .then(function(stream) {
    // var mediaStreamSource = audioContext.createMediaStreamSource(stream);
    // mediaStreamSource.connect(audioContext.destination);
    video.srcObject = stream;
  })
  .catch(function(err) {
    alert(`getUserMedia() is not supported by your browser. ${err}`);
    console.log(`Something went wrong! ${err}`);
  });
}
