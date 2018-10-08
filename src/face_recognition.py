import face_recognition
from os import listdir


class FaceRecogniser():

    def __init__(self):
        self.face_encodings = []
        self.face_names = []
        self.initialised = False

    def init_face_index(self, data_path):
        files = [f for f in listdir(data_path) if f.endswith("jpg")]
        self.face_names = [f.split(".")[0] for f in files]
        images = [face_recognition.load_image_file("{0}/{1}".format(data_path, f)) for f in files]
        for im in images:
            face_locations = face_recognition.face_locations(im)
            self.face_encodings.append(face_recognition.face_encodings(im, face_locations)[0])
        self.initialised = True

    def get_faces(self, image):
        new_image = face_recognition.load_image_file(image)
        im_width = new_image.shape[1]
        im_height = new_image.shape[0]

        face_locations = face_recognition.face_locations(new_image)
        face_encodings = face_recognition.face_encodings(new_image, face_locations)

        faces = []
        for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            matches = face_recognition.compare_faces(self.face_encodings, encoding)

            if True in matches:
                idx = matches.index(True)
                name = self.face_names[idx]

            face = {}
            face["name"] = str(name)
            face["height"] = float((bottom - top)/im_height)
            face["width"] = float((right - left)/im_width)
            face["y"] = float(top/im_height)
            face["x"] = float(left/im_width)

            faces.append(face)

        return faces
