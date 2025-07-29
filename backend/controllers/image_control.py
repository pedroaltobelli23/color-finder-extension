import pandas as pd
import cv2
import base64
import numpy as np
import json
from utils.quantization import image_quantization

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
            
            nparr = np.frombuffer(img_base64, np.uint8)
            img_raw = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            image = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)
            print(f"The type of this input is {type(image)}")
            print(f"Shape: {image.shape}")
            print("Doing image quantizaion...", end="\n")
            
            resized_image, quantized_image, name_quantColorRGB = image_quantization(image, 5)
            
            print("Process endend")
            
            result = {
                "resized_image": cls.decode_array_to_base64(resized_image),
                "quantized_image": cls.decode_array_to_base64(quantized_image),
                "colors": name_quantColorRGB
            }
            
            return json.dumps(result)
        except Exception as e:
            df = pd.DataFrame({"col1":[1,2,3,4,5], "col2":[5,4,3,2,1]})
            json_response = df.to_json(orient="records")
            print(f"Error decoding image: {e}")
            return json_response
        
        
    @classmethod
    def decode_array_to_base64(cls, array: np.ndarray):
        _, buffer = cv2.imencode('.jpg', array)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        return jpg_as_text
    