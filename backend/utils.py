import numpy as np
from PIL import Image

def preprocess_image(img_path, img_size=(224, 224)):
    """Load and preprocess an image for model prediction."""
    img = Image.open(img_path).resize(img_size)
    img_array = np.array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

def predict_image(model, img_path, img_size, class_names):
    """Load a single image, run prediction, and return the predicted class and confidence."""
    img_array = preprocess_image(img_path, img_size)
    predictions = model.predict(img_array)[0]
    class_idx = int(np.argmax(predictions))
    confidence = float(predictions[class_idx])
    return class_names[class_idx], confidence
