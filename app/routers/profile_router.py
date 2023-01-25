from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPBearer

from ..services.microsoft_graph_service import MicrosoftGraphService
from ..dependencies import get_microsoft_graph_service
from ..auth.auth_bearer import JWTBearer
from ..models.Profile import Profile

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    dependencies=[Depends(JWTBearer())],
    responses={404: {"description": "Not found"}}
)

@router.get("")
async def get_profile(microsoft_graph_service: MicrosoftGraphService = Depends(get_microsoft_graph_service)) -> Profile:
    return await microsoft_graph_service.get_basic_profile()



