import cv2
import numpy as np

class ObjDetectNet:
    def __init__(self):
        net = None
        CLASSES = None
        model_initialised = False

    def init_model(self, wghs, cfg, clss):
        self.net = cv2.dnn.readNet(wghs, cfg)
        with open(clss, 'r') as f:
            self.CLASSES = [line.strip() for line in f.readlines()]
        self.model_initialised = True

    def get_output_layers(self):

        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        return output_layers

    def get_objects(self, image, threshold=0.5):

        if not self.model_initialised:
            raise RuntimeError("Model not initialised")

        cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        width = cv2_image.shape[1]
        height = cv2_image.shape[0]
        scale = 0.00392
        net_shape = (416,416)

        blob = cv2.dnn.blobFromImage(cv2.resize(cv2_image, net_shape), scale, net_shape,
                                    (0,0,0), True, crop=False)

        self.net.setInput(blob)

        outs = self.net.forward(self.get_output_layers())

        objects = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > threshold:
                    obj = {}
                    obj["name"] = str(self.CLASSES[class_id])
                    obj["height"] = float(detection[3])
                    obj["width"] = float(detection[2])
                    obj["score"] = float(confidence)
                    # (x,y) is the center, transforme it to the upper-left corner
                    obj["y"] = float(detection[1] - 0.5*obj["height"])
                    obj["x"] = float(detection[0] - 0.5*obj["width"])

                    objects.append(obj)
        return objects
