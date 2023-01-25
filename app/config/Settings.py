from pydantic import BaseSettings

class Settings(BaseSettings):
    tenant_id: str = None
    client_id: str = None
    client_secret: str = None
    audience: str = None
    
    class Config:
        env_file = '.env'
        