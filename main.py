from fastapi import FastAPI
import uvicorn
from src.routers.users import router
app = FastAPI(title="User Management API")
app.include_router(router)
@app.get("/")
async def root():
    return {"message": "User Management API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)