from typing import Generator
import pytest
from httpx import AsyncClient

from app.models.user import User
from app.utils.auth import get_password_hash

user_1 = {
    "id": "634cd28b6f3c8f9a18cf3d45",
    "email": "test@example.com",
    "company": "test-company",
    "password": "test",
    "roles": ["user"],
}


@pytest.fixture(scope='module')
async def setup_test_user():
    new_user_1 = User(**user_1)  # type: ignore
    new_user_1.password = get_password_hash(new_user_1.password)
    try:
        await new_user_1.save()
        yield
    finally:
        await User.delete_all()


async def test_search_users_all(setup_test_user: Generator, client: AsyncClient):
    response_1 = await client.get("/api/v1/users")
    assert response_1.status_code == 200
    res_json = response_1.json()
    assert len(res_json) == 1
    assert res_json[0]["email"] == user_1.get('email')
    assert res_json[0]["company"] == user_1.get('company')
    assert res_json[0]["roles"] == user_1.get('roles')
    assert res_json[0]["_id"] == str(user_1.get('id'))

testdata = [("?email=does-not-exist@example.com", 0),
            ("?email=test@example.com", 1),
            ("?company=does-not-exist-co", 0),
            ("?company=test-company", 1),
            ("?company=test-company&email=test@example.com", 1),
            ("?company=test-company&email=does-not-exist@example.com", 0)
            ]


@pytest.mark.parametrize(("query_params", "expected_len"), testdata)
async def test_search_users_query_params(setup_test_user: Generator, client: AsyncClient, query_params: str, expected_len: int):
    response = await client.get(f"/api/v1/users{query_params}")
    assert response.status_code == 200
    res_json = response.json()
    assert len(res_json) == expected_len


async def test_get_me_unauthorized(setup_test_user: Generator, client: AsyncClient):
    response = await client.get("/api/v1/users/me", headers={"Authorization": "Bearer test"})
    assert response.status_code == 401


async def test_get_me_authorized(setup_test_user: Generator, client: AsyncClient):
    # login
    login_res = await client.post("/api/v1/auth/login", data={"username": user_1.get('email'), "password": user_1.get('password')})
    access_token = login_res.json().get('access_token')
    response = await client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    res_json = response.json()
    assert res_json.get("email") == user_1.get('email')
    assert res_json.get("company") == user_1.get('company')
    assert res_json.get("roles") == user_1.get('roles')
    assert res_json.get("_id") == str(user_1.get('id'))
