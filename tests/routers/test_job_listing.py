from httpx import AsyncClient
from typing import Generator
from beanie import WriteRules

import pytest

from app.models.job_listing import JobListing
from app.models.user import User
from app.utils.auth import get_password_hash

user_1 = {
    "id": "634cd28b6f3c8f9a18cf3d45",
    "email": "test@example.com",
    "company": "test-company",
    "password": "test",
    "roles": ["user"],
}

job_listing_1 = {
    "id": "634cd28b6f3c8f9a18cf3d46",
    "title": "test-title",
    "description": "test-description",
    "location": "test-location",
    "startDate": "2021-09-01T00:00:00",
    "employmentType": "test-employmentType",
    "createdAt": "2021-09-01T00:00:00",
    "updatedAt": "2021-09-01T00:00:00"
}


@pytest.fixture(scope='module')
async def setup_test_job_listing():
    user = User(**user_1)  # type: ignore
    user.password = get_password_hash(user.password)
    new_job_listing_1 = JobListing(**job_listing_1, createdBy=user)  # type: ignore
    try:
        await new_job_listing_1.save(link_rule=WriteRules.WRITE)
        yield
    finally:
        await JobListing.delete_all()
        await User.delete_all()


async def test_search_job_listings_all(setup_test_job_listing: Generator, client: AsyncClient):
    response_1 = await client.get("/api/v1/job-listings")
    assert response_1.status_code == 200
    res_json = response_1.json()
    assert len(res_json) == 1
    assert res_json[0].get("title") == job_listing_1.get('title')
    assert res_json[0].get("description") == job_listing_1.get('description')
    assert res_json[0].get("location") == job_listing_1.get('location')
    assert res_json[0].get("startDate") == job_listing_1.get('startDate')
    assert res_json[0].get("employmentType") == job_listing_1.get('employmentType')
    assert res_json[0].get("createdAt") == job_listing_1.get('createdAt')
    assert res_json[0].get("updatedAt") == job_listing_1.get('updatedAt')
    assert res_json[0].get("_id") == str(job_listing_1.get('id'))
    assert res_json[0].get("createdBy", {}).get("_id") == str(user_1.get('id'))

testdata = [("?title=does-not-exist", 0),
            ("?title=test-title", 1),
            ("?company=does-not-exist", 0),
            ("?company=test-company", 1),
            ("?location=does-not-exist", 0),
            ("?location=test-location", 1),
            ("?employmentType=does-not-exist", 0),
            ("?employmentType=test-employmentType", 1),
            ("?createdById=634cd28b6f3c8f9a18cf3000", 0),
            ("?createdById=634cd28b6f3c8f9a18cf3d45", 1),
            ("?title=test-title&company=test-company&location=test-location&employmentType=test-employmentType&createdById=634cd28b6f3c8f9a18cf3d45", 1),
            ("?title=does-not-exist&company=test-company&location=test-location&employmentType=test-employmentType&createdById=634cd28b6f3c8f9a18cf3d45", 0),
            ("?title=test-title&company=does-not-exist&location=test-location&employmentType=test-employmentType&createdById=634cd28b6f3c8f9a18cf3d45", 0),
            ("?title=test-title&company=test-company&location=does-not-exist&employmentType=test-employmentType&createdById=634cd28b6f3c8f9a18cf3d45", 0)
            ]


@pytest.mark.parametrize(("query_params", "expected_len"), testdata)
async def test_search_job_listings_query_params(setup_test_job_listing: Generator, client: AsyncClient, query_params: str, expected_len: int):
    response_1 = await client.get(f"/api/v1/job-listings{query_params}")
    assert response_1.status_code == 200
    res_json = response_1.json()
    assert len(res_json) == expected_len


async def test_create_job_listing_unauthorized(setup_test_job_listing: Generator, client: AsyncClient):
    response_1 = await client.post("/api/v1/job-listings", json=job_listing_1)
    assert response_1.status_code == 401


async def test_create_job_listing_authorized(setup_test_job_listing: Generator, client: AsyncClient):
    # login
    login_res = await client.post("/api/v1/auth/login", data={"username": user_1.get('email'), "password": user_1.get('password')})
    access_token = login_res.json().get('access_token')
    headers = {"Authorization": f"Bearer {access_token}"}
    # create job listing
    response_1 = await client.post("/api/v1/job-listings", json=job_listing_1, headers=headers)
    assert response_1.status_code == 201
    res_json = response_1.json()
    assert res_json.get("title") == job_listing_1.get('title')
    assert res_json.get("description") == job_listing_1.get('description')
    assert res_json.get("location") == job_listing_1.get('location')
    assert res_json.get("startDate") == job_listing_1.get('startDate')
    assert res_json.get("employmentType") == job_listing_1.get('employmentType')
    assert res_json.get("createdBy", {}).get("_id") == str(user_1.get('id'))
