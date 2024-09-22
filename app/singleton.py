from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import urllib.parse

class SingletonSession:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            user = "root"
            password = urllib.parse.quote_plus("0413")
            host = "localhost"
            database = "projetodiario"
            connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"

            engine = create_engine(connection_string)
            Session = sessionmaker(bind=engine)
            cls._instance = Session()  # Create a single session instance
        return cls._instance
