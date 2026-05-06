from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator

Base = declarative_base()


class PostgreSQLClient:

    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url,
            pool_pre_ping=True,        # ← tests connection before using it
            pool_recycle=300,          # ← recycle connections every 5 minutes
            pool_size=5,               # ← max 5 connections
            max_overflow=10,           # ← allow 10 extra connections
            connect_args={
                "sslmode":        "require",
                "connect_timeout": 10,
            }
        )
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