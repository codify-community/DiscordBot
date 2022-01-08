import logging

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from src.config import Config

_database: MongoClient = None
database = lambda: _database


async def connect_database():
    global _database
    config = Config()
    connection_args = {
        "zlibCompressionLevel": 7,
        "compressors": "zlib"
    }
    _database = AsyncIOMotorClient(config.databaseURL, **connection_args)

    logging.info("Connect to MongoDB")
