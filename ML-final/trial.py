from deepface import DeepFace


# result = DeepFace.verify(
#   img1_path = "jolie-1.jpg",
#   img2_path = "brad-pitt.jpg",
# )

# print(result)
embedding_objs = DeepFace.represent(
  img_path = "group.jpg"
)

print("Embedding", embedding_objs)


# for embedding_obj in embedding_objs:
#   embedding = embedding_obj["embedding"]
#   assert isinstance(embedding, list)
#   assert (
#     model_name == "VGG-Face"
#     and len(embedding) == 4096
#   )
#   print(embedding)

