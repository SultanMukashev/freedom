from retinaface import RetinaFace

resp = RetinaFace.detect_faces("group.jpg")

print(resp)

import matplotlib.pyplot as plt
faces = RetinaFace.extract_faces(img_path = "group.jpg", align = True)
for face in faces:
  print(type(face))
  plt.imshow(face)
  plt.show()