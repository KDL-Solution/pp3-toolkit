from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator
from fastapi.responses import JSONResponse

import random
import traceback
from session_toolkit import get_resource_content_public, upload_resource_public, login_and_create_session, read_image, array_to_buffer
import cv2
from typing import List, Dict
import logging
import os 

app = FastAPI()

session = login_and_create_session()
logging.basicConfig(
    filename='app.log',  # Log file name
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Log format
)

logger = logging.getLogger(__name__)

RESOURCE_SERVER_URL = os.getenv("RESOURCE_SERVER_URL")

# custom metadata
class MetaData(BaseModel):
    sample: int = 1
    steps: int = -1
    guidanceScale: float = 0.0
    seed: int = -1
    lora: List[str] = []
    
    @field_validator('seed')
    def set_random_seed(cls, v):
        return v if v != -1 else random.randint(0, 2**32 - 1)
    
class Prompt(BaseModel):
    positive: str = ""
    negative: str = ""

class ImageInput(BaseModel):
    prompt: Prompt = Prompt()
    meta: MetaData = MetaData()
    sources: List[int] = []
    targets: List[int] = []
    
class ImageOutput(BaseModel):
    images: List[int]
    meta: MetaData

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Failed to validate request: {exc}")
    # 사용자 정의 응답 반환
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )
    
@app.post("/", response_model=ImageOutput)
def generate_image(request: ImageInput):
    
    logger.info(f"Received request: {request}")
    meta = request.meta
    # 이미지 생성 코드
    # ...
    # 이미지 생성 결과
    temp_img = cv2.imread("snoopy.jpg")
    
    buffer = array_to_buffer(temp_img)
    try:
        res = upload_resource_public(session, "snoopy.jpg", buffer, mime_type="image/jpeg", base_url=RESOURCE_SERVER_URL)
    except Exception as e:
        logger.error(f"Failed to upload image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
    
    id = res.json()["id"]
    result_image = [id]
    
    output = ImageOutput(images=result_image, meta=meta)
    logger.info(f"Generated image: {output.model_dump_json()}")
    return output


if __name__ == "__main__":
    import uvicorn
    import argparse
    parser = argparse.ArgumentParser(description="Start the FastAPI server.")
    parser.add_argument('--port', type=int, default=None, help='Port to run the server on')
    args = parser.parse_args()
    if args.port is None: raise ValueError("Port number must be provided as an argument or an environment variable.")
    uvicorn.run(app, host="0.0.0.0", port=args.port)
    