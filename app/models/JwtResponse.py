from pydantic import BaseModel

class JwtResponse(BaseModel):
    access_token: str | None = None