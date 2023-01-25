from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/health",
    tags=["health"],
    dependencies=[],
    responses={404: {"description": "Not found"}}
)

@router.get("/startup")
async def get_startup():
    return {"status": "ok"}	

@router.get("/readiness")
async def get_readiness():
    return {"status": "ok"}	

@router.get("/liveness")
async def get_liveness():
    return {"status": "ok"}	