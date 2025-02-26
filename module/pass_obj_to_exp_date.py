"""
Expiration Date Detection Module

This module manage the pipeline of sending products to the correct function,
which will be able to detect the expiration date for the spesific product
"""
import torch
import torch.nn as nn
from torch.nn import functional as F
from torchvision import models, transforms
from typing import Tuple, List, Union
from ultralytics import YOLO
from module.products_ocr import products_exp_dates
from module.fruit_veg_freshness import fresh_rotten
from PIL import Image


# TODO:
# 1. **class in detection**
#    - Take from Elya.

def get_transform():
    """
    Returns the image transformation pipeline for preprocessing the input image.
    """
    return transforms.Compose([
        transforms.Resize(256),  # Resize to 256x256
        transforms.CenterCrop(224),  # Crop to 224x224 (the input size for ResNet)
        transforms.ToTensor(),  # Convert the image to a tensor
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize to ImageNet stats
    ])

def find_exp_date(
    detections: List[Tuple[int,int,Tuple[int, int, int, int], Image.Image]], class_list: List[str]
)-> List[Union[
        Tuple[int, int, Tuple[int, int, int, int], Image.Image],  # Shelf
        Tuple[int, int, str]  # products
    ]]:
    """
    Determines right function to pass the object to, depending on type.
    Return: updated list with expiration dates for each detected object.
    """
    if len(detections) == 1:  # No objects detected, only shelf
        return detections
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    transform=get_transform()

    model_date_path = "models/DateDetection.pt"
    model_date_detect = YOLO(model_date_path)
    model_date_detect.eval()

    model_freshness_path = "models/freshness_detection.pth"
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, 1000)  # Adjust to match the original model's output units
    model.load_state_dict(torch.load(model_freshness_path, map_location=device))
    model.eval()

    # Create a new model with the correct final layer
    model_freshness_detect = models.resnet18(pretrained=True)
    model_freshness_detect.fc = nn.Linear(model_freshness_detect.fc.in_features, 2)  # Adjust to match the desired output units

    # Copy the weights and biases from the loaded model to the new model
    model_freshness_detect.fc.weight.data = model.fc.weight.data[0:2]  # Copy only the first 2 output units
    model_freshness_detect.fc.bias.data = model.fc.bias.data[0:2]

    # Set the model to evaluation mode and move it to the selected device
    model_freshness_detect.to(device).eval()
    for i in range(1, len(detections)):  # Skip first detection (fridge frame)
        # for now, cheese is the only closed product we have in dataset
        if  detections[i][1] == 5:  
            print("--------------------")
            print("cheese")
            print("--------------------")
            product_img=detections[i][3]
            exp_date = products_exp_dates(model_date_detect, product_img)
            print(f"Cheese expiration date: {exp_date}")
            print("--------------------")
        else:
            class_id = detections[i][1]
            identifier = class_list[class_id]
            product_img=detections[i][3]
            image = transform(product_img).unsqueeze(0)
            # Define class names
            class_names = ['Fresh', 'Rotten']
            # Disable gradient calculations since we are not training
            with torch.no_grad():
                output = model_freshness_detect(image)  # Forward pass through the model

                # Apply softmax to get probabilities (confidence levels)
                probabilities = F.softmax(output, dim=1)

                # Get the predicted class (index with the highest probability)
                _, predicted_class = torch.max(probabilities, 1)

                # Get the confidence level of the predicted class
                confidence = probabilities[0][predicted_class.item()]
                predicted_class_name = class_names[predicted_class.item()]
            exp_date = fresh_rotten(identifier, detections[i][3], confidence)
        if None != exp_date:
            exp_date = exp_date.strftime("%Y-%m-%d")
        detections[i] = (detections[i][0], detections[i][1],detections[i][2], exp_date)

    return detections  #id,class,exp_date
