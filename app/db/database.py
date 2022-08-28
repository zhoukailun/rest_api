from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "dc_assets.db")

# SQLite path
sqlite_url = "sqlite:///" + db_path

# SQLAlchemy
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=True)

DbSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
