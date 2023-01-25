from functools import lru_cache
from fastapi import Request, Depends

from .config import Settings
from .services import IAMService
from .services import MicrosoftGraphService

@lru_cache()
def get_settings():
    return Settings()

async def get_iam_service(request: Request, settings: Settings = Depends(get_settings)):
    service = IAMService(request, settings)
    return service

async def get_microsoft_graph_service(iam_service: IAMService = Depends(get_iam_service)):
    service = MicrosoftGraphService(iam_service)
    return service