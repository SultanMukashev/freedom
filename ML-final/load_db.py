from deepface import DeepFace
from deepface.commons import distance as dst

import pickle
import numpy as np
target_path = "person1.png"
target_img = DeepFace.extract_faces(img_path = target_path)[0]["face"]
target_representation = DeepFace.represent(img_path = target_path, model_name = "VGG-Face")[0]["embedding"]

#load representations of faces in database
f = open("representations.pkl", "rb")
representations = pickle.load(f)
 
distances = []
for i in range(0, len(representations)):
 source_name = representations[i][0]
 source_representation = representations[i][1]
 print(source_name)
 distance = dst.findCosineDistance(source_representation, target_representation)
 print(source_name, ": ",distance)
 distances.append(distance)
#find the minimum distance index

idx = np.argmin(distances)
matched_name = representations[idx][0]