from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
from src.routers.users import router

app = FastAPI(title="User Management API")
app.include_router(router)

INDEX = Path(__file__).resolve().parent / "static" / "index.html"
# image_path = Path(__file__).resolve().parent / "static" / "image.jpg"

@app.get("/",response_class=FileResponse)
async def root():
    return FileResponse(INDEX)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)