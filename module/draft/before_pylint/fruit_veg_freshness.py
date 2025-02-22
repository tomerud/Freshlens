from ultralytics import YOLO
from PIL import Image
from pre_proccess import resize_with_letterbox
from datetime import datetime, timedelta

# TODO:
# 1. **Resize**
#    - make sure Resizing to the size trained on

# 2. **calculating the exp date based on scale**
#    - expand the number of fruits and veg
#    - fix the base shelf life of the products
#    - cls = int(box.cls[0])  Class ID (0 for Fresh, 1 for Rotten - might need to fix)

# 3. expiration date formating:
#    - make sure yyyy-mm-dd
#    - tomer : is it datetime or str?


def estimate_expiration(fruit: str, freshness_label: str, confidence: float) -> datetime:
    #  Recive fruit/veg type and freshness score and calcualte expiration
    #  Return: calculated expiration date

    # Base shelf lives (in days) for the fruit when fresh. These numbers are approximate.
    shelf_life = {
        "banana": 5,   # bananas typically ripen and over-ripen quickly
        "apple": 30,   # apples can last quite a while
        "orange": 14,  # oranges fall in between
    }
    
    # If the fruit is classified as Rotten, we assume it has already expired.
    # We choose to say it expired x days ago depending on how 'rotten' it is.
    if label == "Rotten":
            # Subtract extra days based on confidence:
            if conf < 0.8:
                days_past = 2
            elif conf < 0.9:
                days_past = 3
            elif conf < 0.95:
                days_past = 4
            else:
                days_past = 5

            expiration_date = datetime.today() - timedelta(days=days_past)
    else:
        # For fresh fruits, we start with a base shelf life.
        base_life = shelf_life[fruit]
        
        # Adjust shelf life based on confidence
        if confidence >= 0.9:
            multiplier = 1.0
        elif confidence >= 0.8:
            multiplier = 0.9
        elif confidence >= 0.7:
            multiplier = 0.8
        else:
            multiplier = 0.7  
        
        estimated_days = int(base_life * multiplier)
        expiration_date = datetime.today() + timedelta(days=estimated_days)
        
    return expiration_date

def fresh_rotten(model: YOLO, produce: Image.Image, identifier_type: str):
    #  Detect whether a produce is fresh or rotten and estimate its expiration date.
    #  Return: return expiration date

    # Preprocess the image 
    resized_img, _, _, _ = resize_with_letterbox(produce, target_size=768)
    
    results = model.predict(resized_img)
    
    if results and results[0].boxes:
        box = results[0].boxes[0]
        cls = int(box.cls[0])   # Class ID (0 for Fresh, 1 for Rotten - might need to fix)
        conf = float(box.conf[0])
        
        label = "Fresh" if cls == 0 else "Rotten"
        
        expiration_date = estimate_expiration(identifier_type, label, conf)
        
        return expiration_date
    else:
        return -1 # error

# Example usage:
if __name__ == "__main__":

    
    fruit_type = "apple"  # could be "banana" or "orange"
    try:
        label, conf, exp_date = fresh_rotten(model, product_img, fruit_type)
        print(f"Detected: {label} with confidence {conf:.2f}")
        print(f"Estimated expiration date: {exp_date.strftime('%Y-%m-%d')}")
    except ValueError as e:
        print(e)
