from flask import Flask, request, jsonify
from deepface import DeepFace
import os

app = Flask(__name__)

# Configure paths
db_path = "db"  # Path to the database containing face embeddings
upload_folder = "uploads"  # Folder to temporarily store uploaded images

# Ensure upload folder exists
os.makedirs(upload_folder, exist_ok=True)

@app.route("/find", methods=["POST"])
def find_faces():
    if "files" not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist("files")

    if not files:
        return jsonify({"error": "No files selected"}), 400

    all_results = []

    try:
        for file in files:
            # Save each uploaded file
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)

            # Perform face search using DeepFace
            dfs = DeepFace.find(img_path=file_path, db_path=db_path)

            # Collect results for this file
            results = []
            for df in dfs:
                results.append(df.head().to_dict(orient="records"))

            all_results.append({"file": file.filename, "results": results})

            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            print(all_results)

        return jsonify({"results": all_results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
