import pytest_asyncio
from beanie import init_beanie
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import CONFIG
from app.models.job_application import JobApplication
from app.models.job_listing import JobListing
from app.models.user import User
from app.server import app


@pytest_asyncio.fixture
async def client():
    db_client = AsyncIOMotorClient(CONFIG.MONGO_URI)
    await init_beanie(database=db_client.dev, document_models=[JobApplication, JobListing, User])
    async with AsyncClient(app=app, base_url="http://test") as _client:
        yield _client
