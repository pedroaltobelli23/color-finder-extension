from fastapi import APIRouter, Request, Response
from typing import Optional
from fastapi.responses import JSONResponse
from controllers.image_control import ImageControl

api_image = APIRouter(prefix="/image")

@api_image.get(
    "/",
    description="Sample get",
    tags=["Image"],
    status_code=200
)
async def get_image():
    try:
        json = ImageControl.select()
        res = Response(content=json, media_type="application/json")
        return res
    except Exception as e:
        print("Error")
        
@api_image.post(
    "/quantization",
    description="Return quantizated image and all the colors in it",
    tags=["Image"],
    status_code=200
)
async def post_image(img_dict: dict):
    try:
        print(img_dict)
        json = ImageControl.quantization(img_dict)
        res = Response(content=json, media_type="application/json")
        return res
    except Exception as e:
        print("Error")
      