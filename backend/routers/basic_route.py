from fastapi import APIRouter, Request, Response
from typing import Optional
from fastapi.responses import JSONResponse
from controllers.basic_control import BasicControl

api_basic = APIRouter(prefix="/basic")

@api_basic.get(
    "/",
    description="Faz o get",
    tags=["Basic"],
    status_code=200
)
async def get_basic():
    try:
        json = BasicControl.select()
        res = Response(content=json, media_type="application/json")
        return res
    except Exception as e:
        print("Error own my gawl")