import config
import json
from PIL import Image
from flask import Flask, request, make_response, render_template
from flask import redirect, url_for, jsonify
from src.object_detection import ObjDetectNet
from src.face_recognition import FaceRecogniser

app = Flask(__name__)

obj_det_net = ObjDetectNet()
obj_det_net.init_model(config.ODM_WEIGHTS, config.ODM_CONFIG, config.ODM_CLASSES)

face_recognizer = FaceRecogniser()
face_recognizer.init_face_index(config.FACES_PATH)

@app.route("/")
def index():
    return make_response(render_template("index.html"))

@app.route("/obj_detect")
def object_detection():
    return make_response(render_template("object_detection.html"))

@app.route("/face_recognition")
def face_recognition():
    return make_response(render_template("face_recognition.html"))

@app.route("/api/<api_method>", methods=["POST"])
def detect_api(api_method):
    if request.method == "POST":
        try:
            response = {"status": "fail"}
            image_file = request.files["image"]

            if api_method == "face_recog":
                elements = face_recognizer.get_faces(image_file)

            if api_method == "obj_detect":
                threshold = request.form.get("threshold")
                if threshold is None:
                    threshold = 0.6
                else:
                    threshold = float(threshold)
                image_object = Image.open(image_file)
                elements = obj_det_net.get_objects(image_object, threshold)

            if elements:
                response["payload"] = list(elements)
                response["status"] = "success"

            return jsonify(response)

        except Exception as e:
            print("POST /{0} error: {1}".format(api_method, e))
            return jsonify({"error": "{}".format(e)})

if __name__ == "__main__":
    if obj_det_net.model_initialised and face_recognizer.initialised:
        app.run(debug=False, host="0.0.0.0")
