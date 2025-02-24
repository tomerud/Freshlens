from typing import Tuple, List, Any
from ultralytics import YOLO
from ClosedProductsOCR import ProductsExpDates
from fruit_veg_freshness import fresh_rotten
# TODO:
# 1. **class in detection**
#    - Take from Elya.

# 2. **logic of func**
#    - decide the correct logic

# 3. **Changing / reuturn**
#    - might be better to detections[i][3]
#    - Change the type hinting - first element is the photo the rest are str




if __name__ == "__main__":
    def find_exp_date(detections:List[Tuple[int, int,Any]],class_list:List[str]) ->List[Tuple[int,int,Tuple[int, int, int, int],str]]:  
    # the function is responsible to manage to what function the image is passed on for analysis
    # Returns: List of (object_id,class_id,bounding_boxes,exp_date)

        if (len(detections)==1): # mean didnt detect any objects, detections[0] is the shelf
            return detections

        model_date_path = "Models/DateDetection.pt"
        model_date_detect = YOLO(model_date_path)
        model_date_detect.eval()

        model_Freshness_path = "Models/FreshnessDetection.pt"
        model_Freshness_detect = YOLO(model_Freshness_path)
        model_Freshness_detect.eval()
    
    
        full_exp=(0,5) #tomatos / banana?

        for i in range(1, len(detections)): # the first object in detection is the full frame of the fridge, without detection
            if detections[i][1] in full_exp: #fruits and veg that have been fully implamented exp_date detection
                exp_date = kmeans_expdate(detections[i])
            elif 0<=detections[i][1]<=10:
                class_id = detections[i][1]
                identifier = class_list[class_id]
                exp_date = fresh_rotten(model_Freshness_detect,detections[i][3],identifier)
            else:
                exp_date = ProductsExpDates(model_date_detect,detections[i][3])
            detections[i] = (detections[0],detections[1],detections[2],exp_date)


        
    
              
