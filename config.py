import configparser
import os
from sqlalchemy import create_engine
from supabase import create_client, Client

config = configparser.RawConfigParser()
config.read('config.txt')

DATABASE_URI = config.get('database', 'DATABASE_URI')
engine = create_engine(config.get('database', 'con'))
