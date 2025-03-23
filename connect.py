"""Session configuration file"""
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from config import POSTGRESS_HOST, POSTGRESS_PORT, POSTGRESS_USER, POSTGRESS_PASSWORD

CREDENTIAL = f"{POSTGRESS_HOST}:{POSTGRESS_PORT}"
CONNECTION_PATH =f"{POSTGRESS_USER}:{POSTGRESS_PASSWORD}"
DB_URL = f"postgresql+psycopg2://{CONNECTION_PATH}@{CREDENTIAL}/hw06"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
