from dotenv import load_dotenv, find_dotenv  
from os import getenv
from pymongo import MongoClient

def mongoConnect():
    load_dotenv(find_dotenv())
    uri = getenv('MONGO_URI')
    
    return MongoClient(uri)
