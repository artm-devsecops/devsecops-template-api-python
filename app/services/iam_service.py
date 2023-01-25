from fastapi import Request
import httpx
from ..config import Settings
from ..models import JwtResponse

class IAMService:
    BASE_ADDRESS = 'https://login.microsoftonline.com/'
    
    def __init__(self, request: Request, settings: Settings):
        self.request = request
        self.settings = settings
                
    async def get_on_behalf_of_jwt(self, scope: str) -> JwtResponse:
        authorization = self.request.headers.get('authorization')
        access_token = authorization.replace('Bearer ', '')
        
        form = { 
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id": self.settings.client_id,
            "client_secret": self.settings.client_secret,
            "assertion": access_token,
            "scope": scope,
            "requested_token_use": "on_behalf_of"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{self.BASE_ADDRESS}/{self.settings.tenant_id}/oauth2/v2.0/token', data=form)
            json = response.json()
            return  JwtResponse(**json)

