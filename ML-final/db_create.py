from deepface import DeepFace
import os
#--------------------------
employees = []
 
for r, d, f in os.walk("."): # r=root, d=directories, f = files
   for file in f:
    if (".png" in file):
      exact_path = r + "/" + file
      employees.append(exact_path)
#--------------------------
representations = []
for employee in employees:
 representation = DeepFace.represent(img_path = employee, model_name = "VGG-Face")[0]["embedding"]
 
 instance = []
 instance.append(employee)
 instance.append(representation)
 representations.append(instance)
#--------------------------
import pickle
f = open("representations.pkl", "wb")
pickle.dump(representations, f)
f.close()