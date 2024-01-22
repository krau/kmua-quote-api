import io
import time

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from loguru import logger

from kmua_quote_api.config import settings
from kmua_quote_api.generate import generate_quote_img

app = FastAPI(
    title="kmua Quote API",
    description="API for kmua quote",
    version="0.1.0",
)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.debug(f"{request.method} {request.url} {process_time}s")
    return response


@app.post(
    "/generate",
    description="Generate quote image",
    tags=["generate"],
    response_description="Quote image",
    response_class=StreamingResponse,
)
async def generate(
    avatar: UploadFile = File(...),
    text: str = Form(..., max_length=200),
    name: str = Form(..., max_length=64),
) -> StreamingResponse:
    if len(text) > 200:
        raise HTTPException(
            status_code=400, detail="Text must be less than 200 characters"
        )
    if len(name) > 64:
        raise HTTPException(
            status_code=400, detail="Name must be less than 64 characters"
        )
    if avatar.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Avatar must be png or jpeg")
    if avatar.size > 1024 * 1024 * 2:
        raise HTTPException(status_code=400, detail="Avatar must be less than 2MB")
    avatar = await avatar.read()
    img = generate_quote_img(avatar, text, name)
    img_byte_arr = io.BytesIO(img)
    return StreamingResponse(img_byte_arr, media_type="image/png")


if __name__ == "__main__":
    host = settings.get("host", "0.0.0.0")
    port = settings.get("port", 39090)
    uvicorn.run(app, host=host, port=port)
