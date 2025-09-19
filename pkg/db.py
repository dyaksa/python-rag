import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_db():

    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )

    return connection
