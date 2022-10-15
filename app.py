from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from config import CONFIG

app = FastAPI(
    title='Hataraki Backend',
    description='Hataraki REST API service',
    version='0.0.1',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # TODO: Configure to frontend URL when deployed
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup_event():
    # init database connection
    db_client = AsyncIOMotorClient(CONFIG.MONGO_URI)
    await init_beanie(db_client, document_models=[])
    print('Connected to MongoDB!')
