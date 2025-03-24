"""Script configuration file"""

import os
from dotenv import load_dotenv

load_dotenv()

POSTGRESS_USER = os.getenv("POSTGRESS_USER", "postgres")
POSTGRESS_PASSWORD = os.getenv("POSTGRESS_PASSWORD", "mysecretpassword")
POSTGRESS_HOST = os.getenv("POSTGRESS_HOST", "localhost")
POSTGRESS_PORT = int(os.getenv("POSTGRESS_PORT", "5432"))
