import uvicorn
from fastapi import FastAPI

from src.settings import settings_file
from src.routers.user import router

app = FastAPI(debug=False)
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings_file.SERVER_ADDR,
        port=settings_file.SERVER_PORT,
        log_level="info"
    )