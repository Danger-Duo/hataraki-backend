import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_users(client: AsyncClient):
    response = await client.get("/api/v1/users?email=hataraki@example.com")
    assert response.status_code == 200
    assert response.json() == [{"_id": "634cf8bd0d5469dfc176c44c", "email": "hataraki@example.com",
                                "company": "Hataraki",
                                "roles": [
                                    "user"
                                ],
                                "createdAt": "2022-10-17T14:39:57.438000",
                                "updatedAt": "2022-10-17T14:39:57.438000"}]
