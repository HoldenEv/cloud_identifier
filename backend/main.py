import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import json

def main():
    # ---------------------------
    # 1) DATA DIRECTORY SETTINGS
    # ---------------------------
    base_dir = os.path.join("data", "train")  # adjust if needed
    img_size = (224, 224)
    batch_size = 32
    validation_split = 0.2  # 20% for validation

    # ---------------------------
    # 2) LOAD DATASETS
    # ---------------------------
    train_ds = keras.preprocessing.image_dataset_from_directory(
        base_dir,
        validation_split=validation_split,
        subset="training",
        seed=42,
        image_size=img_size,
        batch_size=batch_size
    )

    val_ds = keras.preprocessing.image_dataset_from_directory(
        base_dir,
        validation_split=validation_split,
        subset="validation",
        seed=42,
        image_size=img_size,
        batch_size=batch_size
    )

    # Check the class names
    class_names = train_ds.class_names
    print("Detected classes:", class_names)
    with open("class_names.json", "w") as f:
      json.dump(class_names, f)

    num_classes = len(class_names)

    # ---------------------------
    # 3) (OPTIONAL) DATA AUGMENTATION
    # ---------------------------
    # Add random flips/rotations to help generalize
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        # You can add more augmentations like RandomZoom, RandomTranslation, etc.
    ])

    # ---------------------------
    # 4) BUILD A SIMPLE CNN MODEL
    # ---------------------------
    model = keras.Sequential([
        # Normalize the input images from [0..255] to [0..1]
        layers.Rescaling(1./255, input_shape=(img_size[0], img_size[1], 3)),

        # Insert data augmentation layer right after Rescaling
        data_augmentation,

        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D(),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(),
        
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(),
        
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')  # output layer
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.summary()

    # ---------------------------
    # 5) TRAIN THE MODEL
    # ---------------------------
    epochs = 5  # Increase if needed
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    # ---------------------------
    # 6) EVALUATE THE MODEL
    # ---------------------------
    print("Saving model...")
    model.save("cloud_model.h5")
    print("Model saved as cloud_model.h5")
    val_loss, val_acc = model.evaluate(val_ds)
    print(f"\nValidation accuracy: {val_acc:.2f}")

    # ---------------------------
    # 7) PREDICT ON A SINGLE IMAGE
    # ---------------------------
    test_image_path = "./data/test/1.jpg"  # put a test image here or change the path

    if os.path.exists(test_image_path):
        predicted_class, confidence = predict_image(
            model=model, 
            img_path=test_image_path, 
            img_size=img_size, 
            class_names=class_names
        )
        while (confidence <= 0.57):
            predicted_class, confidence = predict_image(
                model=model, 
                img_path=test_image_path, 
                img_size=img_size, 
                class_names=class_names
            )
        
        print(f"\nPrediction: {predicted_class} (Confidence: {confidence:.2f})")
    else:
        print("\nNo test image found. Provide a valid image path to predict.")

def predict_image(model, img_path, img_size, class_names):
    """Load a single image and run prediction."""
    img = Image.open(img_path).resize(img_size)
    img_array = np.array(img)
    
    # Scale pixel values to [0, 1] if model expects that
    img_array = img_array / 255.0
    
    # Add a batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    # Get prediction
    predictions = model.predict(img_array)[0]
    class_idx = np.argmax(predictions)
    confidence = predictions[class_idx]
    return class_names[class_idx], confidence

if __name__ == "__main__":
    main()
