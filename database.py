import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

ssl_args = {
    "ssl": {
        "ssl_ca": "./DigiCertGlobalRootCA.crt.pem",
        "ssl_g2": "./DigiCertGlobalRootG2.crt.pem",
        "ssl_Au": "./Microsoft RSA Root Certificate Authority 2017.crt"
    }
}

engine = create_engine(DATABASE_URL, connect_args=ssl_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# print("DB_USER:", DB_USER)
# print("DB_PASSWORD:", DB_PASSWORD)
# print("DB_HOST:", DB_HOST)
# print("DB_PORT:", DB_PORT)
# print("DB_NAME:", DB_NAME)

# DATABASE_URL = "sqlite:///./product_master.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DATABASE_URL = "mysql+pymysql://youruser@rdbs-002-gen10-step3-1-oshima3:yourpassword@rdbs-002-gen10-step3-1-oshima3.mysql.database.azure.com/yourdbname"
# DATABASE_URL = "mysql+pymysql://youruser:yourpassword@rdbs-002-gen10-step3-1-oshima3.mysql.database.azure.com/pos_db"
# engine = create_engine(DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)