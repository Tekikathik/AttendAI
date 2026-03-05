import sys
import os
import cv2
import pickle
import numpy as np
from datetime import datetime
from mtcnn import MTCNN
from keras_facenet import FaceNet
from sklearn.metrics.pairwise import cosine_similarity

# Arguments from Node.js
file_path = sys.argv[1]
file_type = sys.argv[2]

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


EMBEDDINGS_PATH = os.path.join(BASE_DIR, "..", "embeddings", "all_embeddings.pkl")
CSV_DIR = os.path.join(BASE_DIR, "..", "attendance_csv")



os.makedirs(CSV_DIR, exist_ok=True)

# Load models
detector = MTCNN()
embedder = FaceNet()

# Load embeddings
with open(EMBEDDINGS_PATH, "rb") as f:
    known_embeddings = pickle.load(f)

# Read image
image = cv2.imread(file_path)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

faces = detector.detect_faces(rgb)
print(f"Faces detected: {len(faces)}")

present_students = set()

for face in faces:
    x, y, w, h = face["box"]
    face_img = rgb[y:y+h, x:x+w]
    face_img = cv2.resize(face_img, (160, 160))
    face_img = np.expand_dims(face_img, axis=0)

    embedding = embedder.embeddings(face_img)[0]

    best_match = None
    best_score = 0.0

    for student_id, emb_list in known_embeddings.items():
        for known_emb in emb_list:
            score = cosine_similarity([embedding], [known_emb])[0][0]
            if score > best_score:
                best_score = score
                best_match = student_id

    if best_score > 0.6:  # threshold
        present_students.add(best_match)
        print(f"Matched: {best_match}")

# Create CSV
date = datetime.now().strftime("%Y-%m-%d")
time = datetime.now().strftime("%H:%M")

csv_path = f"{CSV_DIR}/attendance_{date}.csv"

with open(csv_path, "w") as f:
    f.write("date,student_id,status,time\n")
    for student in known_embeddings.keys():
        status = "Present" if student in present_students else "Absent"
        f.write(f"{date},{student},{status},{time if status=='Present' else '-'}\n")

print("Attendance CSV saved:", csv_path)