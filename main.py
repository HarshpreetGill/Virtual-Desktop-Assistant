import os
import gd2
from PIL import Image
from keras.models import load_model
import numpy as np
from numpy import asarray
from numpy import expand_dims
from keras_facenet import FaceNet
import pickle
import cv2 

def get_name():
    HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))
    MyFaceNet = FaceNet()

    myfile = open("data.pkl", "rb")
    database = pickle.load(myfile)
    myfile.close()
    cap = cv2.VideoCapture(0)
    person_names = {}
    count = 0
    while (count < 20):
        _, gbr1 = cap.read()
        wajah = HaarCascade.detectMultiScale(gbr1, 1.1, 4)
        if len(wajah) > 0:
            x1, y1, width, height = wajah[0]
        else:
            x1, y1, width, height = 1, 1, 10, 10
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        gbr = Image.fromarray(gbr)  
        gbr_array = asarray(gbr)

        face = gbr_array[y1:y2, x1:x2]
        face = Image.fromarray(face)
        face = face.resize((160, 160))
        face = asarray(face)
        face = expand_dims(face, axis=0)
        signature = MyFaceNet.embeddings(face)
        min_dist = 100
        identity = ' '
        for key, value in database.items():
            dist = np.linalg.norm(value - signature)
            if dist < min_dist:
                min_dist = dist
                identity = key
        
        if min_dist > 1:  # Threshold for identification
            print("User not identified. Terminating...")
            cv2.destroyAllWindows()
            cap.release()
            return None

        cv2.putText(gbr1, identity, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.rectangle(gbr1, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('res', gbr1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

        if identity in person_names:
            person_names[identity] += 1
        else:
            person_names[identity] = 0

        count += 1
    ncnt = 0
    for name, cnt in person_names.items():
        if cnt > ncnt:
            ncnt = cnt
            pname = name
    cv2.destroyAllWindows()
    cap.release()
    return pname

def main():
    person_name = get_name()
    if person_name:
        gd2.wishMe(person_name)
        gd2.listenCommand()

if __name__ == "__main__":
    main()

    
