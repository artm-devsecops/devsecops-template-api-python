import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .routers import health_router, profile_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

app.include_router(health_router.router)
app.include_router(profile_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)