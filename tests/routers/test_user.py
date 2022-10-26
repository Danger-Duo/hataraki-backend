import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.fixture(scope='module')
async def loaded_client(client: AsyncClient):
    new_user_1 = User(id="634cd28b6f3c8f9a18cf3d45", email="test@example.com",  # type: ignore
                      company="test-company", password="test")
    try:
        await new_user_1.save()
        yield client
    finally:
        await User.delete_all()


async def test_search_users_all(loaded_client: AsyncClient):
    new_user_1 = User(id="634cd28b6f3c8f9a18cf3d45", email="test@example.com",  # type: ignore
                      company="test-company", password="test")
    response_1 = await loaded_client.get("/api/v1/users")
    assert response_1.status_code == 200
    res_json = response_1.json()
    assert len(res_json) == 1
    assert res_json[0]["email"] == new_user_1.email
    assert res_json[0]["company"] == new_user_1.company
    assert res_json[0]["roles"] == new_user_1.roles
    assert res_json[0]["_id"] == str(new_user_1.id)


@pytest.mark.parametrize(("query_params", "expected"),
                         [("?email=does-not-exist@example.com", 0),
                          ("?email=test@example.com", 1),
                          ("?company=does-not-exist-co", 0),
                          ("?company=test-company", 1),
                          ("?company=test-company&email=test@example.com", 1),
                          ("?company=test-company&email=does-not-exist@example.com", 0)
                          ])
async def test_search_users_query_params(loaded_client: AsyncClient, query_params: str, expected: int):
    new_user_1 = User(id="634cd28b6f3c8f9a18cf3d45", email="test@example.com",  # type: ignore
                      company="test-company", password="test")
    try:
        await new_user_1.save()

        response = await loaded_client.get(f"/api/v1/users{query_params}")
        assert response.status_code == 200
        res_json = response.json()
        assert len(res_json) == expected

    finally:
        await new_user_1.delete()
