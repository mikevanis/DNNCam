import cv2
import numpy as np
from imutils.video import WebcamVideoStream
import imutils
import time

vs = WebcamVideoStream(src=0).start()

rows = open("synset_words.txt").read().strip().split("\n")
classes = [r[r.find(" ") + 1:].split(",")[0] for r in rows]

while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    elif key == ord('p'):
        # send to DNN.
        blob = cv2.dnn.blobFromImage(frame, 1, (224, 224), (104, 117, 123))
        print("Loading model...")
        net = cv2.dnn.readNetFromCaffe("bvlc_googlenet.prototxt", "bvlc_googlenet.caffemodel")
        net.setInput(blob)
        start = time.time()
        predictions = net.forward()
        end = time.time()
        print("Classification took {:.5} seconds".format(end - start))
        indices = np.argsort(predictions[0])[::-1][:5]

        for(i, index) in enumerate(indices):

            if i == 0:
                text = "{}, {:.2f}%".format(classes[index], predictions[0][index] * 100)
                cv2.putText(frame, text, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            print("{}. label: {}, probability: {:.5}".format(i + 1, classes[index], predictions[0][index]))

        cv2.imshow("Classification", frame)

cv2.destroyAllWindows()
vs.stop()
