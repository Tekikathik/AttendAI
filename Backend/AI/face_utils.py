import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

THRESHOLD = 0.65

def recognize_face(face_embedding, known_embeddings):
    best_match = None
    best_score = 0

    for student_id, emb_list in known_embeddings.items():
        for emb in emb_list:
            score = cosine_similarity([face_embedding], [emb])[0][0]
            if score > best_score:
                best_score = score
                best_match = student_id

    if best_score > THRESHOLD:
        return best_match
    return None