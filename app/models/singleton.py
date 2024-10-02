from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import urllib.parse

class SingletonSession:
    r"""Classe singleton para iniciar a seção, só presisa ser instanciado uma vez no codigo para continuar utilizando a seção.
        .. code-block:: python
            session = SingletonSession.get_instance()
"""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            user = "root"
            password = urllib.parse.quote_plus("senai@123")
            host = "localhost"
            database = "projetodiario"
            connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"

            engine = create_engine(connection_string)
            
            Session = sessionmaker(bind=engine)
            cls._instance = Session()  # Create a single session instance
        return cls._instance
