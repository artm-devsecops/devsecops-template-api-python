import pytest
from httpx import AsyncClient

from ..main import app
from ..dependencies import get_settings, get_iam_service, get_microsoft_graph_service
from ..config import Settings

def override_get_settings():
    return Settings(audience="audience", tenant_id="tenant_id", client_id="client_id", client_secret="client_secret")

app.dependency_overrides[get_settings] = override_get_settings
#app.dependency_overrides[get_iam_service] = override_get_iam_service()

@pytest.mark.anyio
async def profile_get_basic_profile_returns_a_profile():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
