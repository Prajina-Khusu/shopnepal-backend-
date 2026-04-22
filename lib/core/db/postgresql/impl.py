from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator

Base = declarative_base()


class PostgreSQLClient:

    def __init__(self, database_url: str):
        self.engine       = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        db: Session = self.SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()