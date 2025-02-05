import os


# Configure database credentials using pymysql in Python
class DBConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
        .format(
            username='root',  # Your database username
            password='1234',  # Your database password
            host='127.0.0.1',  # Your database host
            port=3310,  # Your database port
            database='rms-backend'  # Your database name
        )
    )

