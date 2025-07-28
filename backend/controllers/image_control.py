import pandas as pd
import cv2
import base64
import io
import numpy as np
from PIL import Image

class ImageControl:
    @classmethod
    def select(cls)->str:
        df = pd.DataFrame({"col1":[1,2,3,4,5], "col2":[5,4,3,2,1]})
        json_response = df.to_json(orient="records")
        return json_response
    
    @classmethod
    def quantization(cls, img_dict: dict)->str:
        try:
            img_str = img_dict["image"].split(",")[1]
            img_base64 = base64.b64decode(img_str)
            
            # Save it as a file, just for text
            with open("saved_image.png", "wb") as f:
                f.write(img_base64)
            
            nparr = np.frombuffer(img_base64, np.uint8)
            img_raw = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            image = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)
            print(f"The type of this input is {type(image)}")
            print(f"Shape: {image.shape}")
            print("Doing image quantizaion...", end="\n")
            
            return None
        except Exception as e:
            df = pd.DataFrame({"col1":[1,2,3,4,5], "col2":[5,4,3,2,1]})
            json_response = df.to_json(orient="records")
            print(f"Error decoding image: {e}")
            return json_response
    