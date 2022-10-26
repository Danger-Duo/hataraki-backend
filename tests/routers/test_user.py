import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.mark.asyncio
async def test_search_users(client: AsyncClient):
    new_user = User(id="634cd28b6f3c8f9a18cf3d45", email="test@example.com",  # type: ignore
                    company="test-company", password="test")
    try:
        await new_user.save()

        response = await client.get("/api/v1/users")
        assert response.status_code == 200
        res_json = response.json()
        assert len(res_json) == 1
        assert res_json[0]["email"] == new_user.email
        assert res_json[0]["company"] == new_user.company
        assert res_json[0]["roles"] == new_user.roles
        assert res_json[0]["_id"] == str(new_user.id)

    finally:
        await new_user.delete()
