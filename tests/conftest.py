import pytest
from beanie import init_beanie
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import CONFIG
from app.models.job_application import JobApplication
from app.models.job_listing import JobListing
from app.models.user import User
from app.server import app

pytestmark = pytest.mark.anyio  # set anyio as the default test runner


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='package')
async def client(anyio_backend):
    db_client = AsyncIOMotorClient(CONFIG.MONGO_URI)
    await init_beanie(database=db_client.test, document_models=[JobApplication, JobListing, User])
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
