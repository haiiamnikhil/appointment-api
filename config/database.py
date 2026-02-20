from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import load_config_values

config_values = load_config_values()

engine = create_engine(config_values.database_url)

SessionMaker = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
