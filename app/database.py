import os
import asyncio
from aiohttp import web
# from motor.motor_asyncio import AsyncIOMotorClient
import motor.motor_asyncio

def setup_database(app):
    DP_MONGO_SERVER_HOST = os.getenv('DP_MONGO_SERVER_HOST', '127.0.0.1')
    DP_MONGO_SERVER_PORT = os.getenv('DP_MONGO_SERVER_PORT', '27017')
    DP_MONGO_SERVER_DATABASE = os.getenv('DP_MONGO_SERVER_DATABASE', 'test_database')
    client = motor.motor_asyncio.AsyncIOMotorClient(DP_MONGO_SERVER_HOST, int(DP_MONGO_SERVER_PORT))
    # Add database to the base app    
    app['db'] = client[DP_MONGO_SERVER_DATABASE]

