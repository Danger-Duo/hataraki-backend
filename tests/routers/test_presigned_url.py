import boto3
import pytest
import requests
from beanie import WriteRules
from httpx import AsyncClient

from app.config import CONFIG
from app.models.user import User
from app.utils.auth import get_password_hash

test_object_key_1 = 'test'

user_1 = {
    "id": "634cd28b6f3c8f9a18cf3d45",
    "email": "test@example.com",
    "company": "test-company",
    "password": "test",
    "roles": ["user"],
}


@pytest.fixture(scope='module')
def s3_client():
    s3_boto3_client = boto3.client("s3", aws_access_key_id=CONFIG.AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=CONFIG.AWS_SECRET_ACCESS_KEY,
                                   endpoint_url=CONFIG.S3_ENDPOINT_URL)
    yield s3_boto3_client


@pytest.fixture(scope='module')
async def setup_test_presigned_url(s3_client):
    try:
        user = User(**user_1)  # type: ignore
        user.password = get_password_hash(user.password)
        await user.save(link_rule=WriteRules.WRITE)

        # create bucket
        s3_client.create_bucket(Bucket=CONFIG.S3_BUCKET_NAME)

        # insert object
        s3_client.put_object(Bucket=CONFIG.S3_BUCKET_NAME, Key=test_object_key_1, Body='test')

        yield

    finally:
        # delete object
        s3_client.delete_object(Bucket=CONFIG.S3_BUCKET_NAME, Key=test_object_key_1)

        # delete user
        await User.delete_all()

        # delete bucket
        s3_client.delete_bucket(Bucket=CONFIG.S3_BUCKET_NAME)


async def test_generate_download_presigned_url(setup_test_presigned_url, client: AsyncClient):
    # login
    login_res = await client.post("/api/v1/auth/login", data={"username": user_1.get('email'), "password": user_1.get('password')})
    access_token = login_res.json().get('access_token')
    headers = {"Authorization": f"Bearer {access_token}"}

    # generate presigned url
    response = await client.get(f'/api/v1/presigned-url?key={test_object_key_1}', headers=headers)
    assert response.status_code == 200
    assert 'presignedUrl' in response.json()


async def test_generate_upload_presigned_url_key_exists(setup_test_presigned_url, client: AsyncClient):
    # generate presigned url
    response = await client.post(f'/api/v1/presigned-url/upload', json={"key": test_object_key_1, "contentType": "text/plain"})
    assert response.status_code == 400


async def test_generate_upload_presigned_url_missing_content_type(setup_test_presigned_url, client: AsyncClient):
    # generate presigned url
    response = await client.post(f'/api/v1/presigned-url/upload', json={'invalidKey': 'invalidVal'})
    assert response.status_code == 422


async def test_generate_upload_presigned_url_valid(setup_test_presigned_url, s3_client, client: AsyncClient):
    # generate presigned url
    response = await client.post(f'/api/v1/presigned-url/upload', json={'key': 'requirements.txt'})
    assert response.status_code == 201
    presigned_url = response.json().get('presignedUrl')
    fields = response.json().get('fields')
    assert presigned_url is not None
    assert fields is not None
    try:
        # use requests lib instead as httpx does not work
        response_2 = requests.post(presigned_url, files={'file': (
            'requirements.txt', open('requirements.txt', 'rb'))}, data=fields)
    finally:
        s3_client.delete_object(Bucket=CONFIG.S3_BUCKET_NAME, Key='requirements.txt')

    assert response_2.status_code == 204
