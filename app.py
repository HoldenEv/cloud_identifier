from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import io
from utils import preprocess_image

app = Flask(__name__)

# ---------------------------
# Load the saved model
# ---------------------------
model = keras.models.load_model("cloud_model.h5")

# Make sure the class names are in the same order as during training.
# You can also save the class_names list to a file during training.
class_names = [
    "cirrus",
    "cumulus",
    "stratus",
    # ... add the rest of your 11 cloud types here in order ...
]

@app.route("/predict", methods=["POST"])
def predict():
    # Check if the post request has the file part
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        # Read the image file and preprocess it
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Run prediction
        predictions = model.predict(img_array)[0]
        class_idx = int(np.argmax(predictions))
        confidence = float(predictions[class_idx])
        label = class_names[class_idx]

        return jsonify({
            "predicted_class": label,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
