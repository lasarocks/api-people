import os
import psycopg2
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



# DB_USER = 'piroka'
# DB_PASSWORD = 'senha@segura'
# DB_HOST = '20.169.148.195'
# DB_PORT = '51220'
# DB_NAME = 'serasa'


# encoded_password = urllib.parse.quote(DB_PASSWORD, safe='')


#SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


RENDER_CONNECTION = os.getenv('RENDERPOSTGRES')


AUX_CONNECTION = 'sqlite:///CPFL-g.db?check_same_thread=False'

#RENDER
SQLALCHEMY_DATABASE_URL = RENDER_CONNECTION if RENDER_CONNECTION else AUX_CONNECTION



#SQLALCHEMY_DATABASE_URL = 

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

#Base = declarative_base(bind=engine)
Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()