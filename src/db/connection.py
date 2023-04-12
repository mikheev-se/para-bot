from sqlalchemy import create_engine
from src.core.settings import settings
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.db_url)

Session = sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
