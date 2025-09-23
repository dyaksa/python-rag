import pymysql
from app.core.config import settings

def db():
    connection = pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )

    return connection
