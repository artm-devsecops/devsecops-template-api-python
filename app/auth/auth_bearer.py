import jwt
import json
import urllib.request

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..config import Settings
from ..dependencies import get_settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request, settings: Settings = Depends(get_settings)):
        self.settings = settings
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.__verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def __verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = self.__decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
    
    # Get the JWKS URL from the OpenID configuration
    # TODO: Cache the JWKS result
    def __get_jwks_url(self, issuer_url: str):
        well_known_url = issuer_url + "/.well-known/openid-configuration"
        with urllib.request.urlopen(well_known_url) as response:
            well_known = json.load(response)
        if not 'jwks_uri' in well_known:
            raise Exception('jwks_uri not found in OpenID configuration')
        return well_known['jwks_uri']

    def __decodeJWT(self, token: str) -> dict:
        try:
            unvalidated = jwt.decode(token, options={"verify_signature": False})
            jwks_url = self.__get_jwks_url(unvalidated['iss'])
            jwks_client = jwt.PyJWKClient(jwks_url)
            header = jwt.get_unverified_header(token)
            key = jwks_client.get_signing_key(header["kid"]).key
            
            decoded_token = jwt.decode(token, key, [header["alg"]], audience=self.settings.audience)
            return decoded_token
        except Exception as err:
            return {}