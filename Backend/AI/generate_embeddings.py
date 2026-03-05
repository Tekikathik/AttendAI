import os
import cv2
import pickle
import numpy as np
from mtcnn import MTCNN
from keras_facenet import FaceNet

DATASET_PATH = "../dataset"
OUTPUT_PATH = "../embeddings/all_embeddings.pkl"

detector = MTCNN()
embedder = FaceNet()

embeddings = {}

for student_id in os.listdir(DATASET_PATH):
    student_path = os.path.join(DATASET_PATH, student_id)
    if not os.path.isdir(student_path):
        continue

    embeddings[student_id] = []

    for img_name in os.listdir(student_path):
        img_path = os.path.join(student_path, img_name)
        image = cv2.imread(img_path)
        if image is None:
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(rgb)
        if len(faces) == 0:
            continue

        x, y, w, h = faces[0]["box"]
        face = rgb[y:y+h, x:x+w]
        face = cv2.resize(face, (160, 160))
        face = np.expand_dims(face, axis=0)

        embedding = embedder.embeddings(face)[0]
        embeddings[student_id].append(embedding)

os.makedirs("../embeddings", exist_ok=True)

with open(OUTPUT_PATH, "wb") as f:
    pickle.dump(embeddings, f)

print("✅ Embeddings generated successfully")