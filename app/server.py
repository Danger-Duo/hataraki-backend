from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import CONFIG
from app.models.user import User
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router

app = FastAPI(
    title='Hataraki Backend',
    description='Hataraki REST API service',
    version='0.0.1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # TODO: Configure to frontend URL when deployed
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user_router)
app.include_router(auth_router)


@app.on_event('startup')
async def startup_event():
    # init database connection
    db_client = AsyncIOMotorClient(CONFIG.MONGO_URI)
    await init_beanie(database=db_client.dev, document_models=[User])
    print('Connected to MongoDB!')
