import os

basedir = os.path.abspath(os.path.dirname(__file__))

class DBConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
        .format(
            username='root',  # Your database username
            password='Ismail%40491',  # Your database password
            host='127.0.0.1',  # Your database host
            port=3306,  # Your database port
            database='mordorestate'  # Your database name
        )
    )
