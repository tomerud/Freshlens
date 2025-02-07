from typing import Tuple, List, Any
from ultralytics import YOLO
from ClosedProductsOCR import ProductsExpDates
# TODO:
# 1. **class in detection**
#    - Take from Elya.

# 2. **logic of func**
#    - decide the correct logic

# 3. **Changing / reuturn**
#    - might be better to detections[i][3]
#    - Change the type hinting - first element is the photo the rest are str

# 3. **exp_date for fruits and veg**
#    - need to implement

model_path = "Models/DateDetection.pt"
model_date_detect = YOLO(model_path)
model_date_detect.eval()

if __name__ == "__main__":
    def find_exp_date(detections:List[Tuple[int, str,Any]]) ->List[Tuple[int,int,Tuple[int, int, int, int],str]]:  
    # the function is responsible to manage to what function the image is passed on for analysis
    # Returns: List of (object_id,class_id,bounding_boxes,exp_date)

    #it is more direct to do it using the class_id, but doing it by the class id \
    #make it less "readable" and constarint the way we add new classes for detections
    
        full_exp=(0,5)
        fruits_and_vegetables= (2,)#"fill other as fitting the dataset of trainnig detections"

        for i in range(1, len(detections)): # the first object in detection is the full frame of the fridge, without detection
            if detections[i][1] in full_exp: #fruits and veg that have been fully implamented exp_date detection
                detections[i] = kmeans_expdate(detections[i])
            elif detections[i][1] in fruits_and_vegetables:
                detections[i] = fresh_rotten(detections[i])
            else:
                detections[i] = ProductsExpDates(model_date_detect,detections[i])


        
    
              
