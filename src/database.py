from contextlib import contextmanager
import logging
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger('__main__')
Base = declarative_base()

class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(
            db_url,
            #connect_args={"check_same_thread": False}
         )
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit = False, 
                autoflush = False, 
                bind = self._engine
            )
        )
    
    def create_database(self):
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self):
        session: orm.Session = self._session_factory()
        try:
            yield session
        except:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
