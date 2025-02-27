import os
from fastapi import FastAPI, UploadFile, File #check and upload the files
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image #helps manipulate the images
import numpy as np
from PIL import Image #Pil is also to manipulate image
import io

app = FastAPI() #helps create the routes

@app.get("/")
async def read_root():

    return {
        "message": "Welcome to the Fashion MNIST API!.This model is able to predict the images uploaded depending on the class names indicated in the dataset",
        "instructions": {
            "POST /predict/": "Upload a grayscale image of a handwritten digit (28x28 pixels) to get the predicted class."
        }
    }

# Ensure the model file exists
model_path = 'Fashion_mnist.keras'
if not os.path.exists(model_path):
    raise ValueError(f"Model file not found: {model_path}")

# Load the trained model
model = load_model(model_path)

# Define class names for Fashion mnist dataset
class_names = ["T-shirt/top","Trouser","Pullover","Dress","Coat","Sandal","Shirt","Sneaker","Bag","Ankle boot"]

def preprocess_image(image_bytes):
    # Open the image
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")#RGB is red blue green
    # Resize the image to 32x32
    img = img.resize((32, 32))
    # Convert the image to a numpy array
    img_array = np.array(img)
    # Normalize the image
    img_array = img_array.astype('float32') / 255.0 
    # Expand dimensions to match the model input shape
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

#creating an endpoint or a route to predict
@app.post("/Clothes")
async def predict(file: UploadFile = File(...)): #async is a function that tells the function to wait for animage to be uploaded
    # Read the image file
    contents = await file.read()
    # Preprocess the image
    img_array = preprocess_image(contents)
    # Make a prediction
    predictions = model.predict(img_array)
    # Get the class with the highest probability
    predicted_class = class_names[np.argmax(predictions[0])]#prediction starting from 0
    return {"predicted_class": predicted_class}

