
import httpx

from ..models import Profile
from ..services.iam_service import IAMService

class MicrosoftGraphService:
    BASE_ADDRESS = 'https://graph.microsoft.com/'
    
    def __init__(self, iam_service: IAMService):
        self.iam_service = iam_service

    async def get_basic_profile(self) -> Profile:
        jwt = await self.iam_service.get_on_behalf_of_jwt(f"{self.BASE_ADDRESS}user.read")    
        
        headers = {
            "Authorization": f"Bearer {jwt.access_token}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.BASE_ADDRESS}/v1.0/me', headers=headers)
            json = response.json()
            return Profile(**json)