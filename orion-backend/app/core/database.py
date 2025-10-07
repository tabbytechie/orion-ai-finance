from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session

# Configure SQLAlchemy engine with connection pooling and timeouts
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Enable connection liveness checks
    pool_size=5,  # Number of connections to keep open
    max_overflow=10,  # Number of connections to create beyond pool_size
    pool_timeout=30,  # Seconds to wait before giving up on getting a connection
    pool_recycle=300,  # Recycle connections after 5 minutes
    connect_args={
        'connect_timeout': 5,  # Connection timeout in seconds
        'keepalives': 1,  # Enable TCP keepalive
        'keepalives_idle': 30,  # Time before sending keepalive
        'keepalives_interval': 10,  # Interval between keepalives
        'keepalives_count': 5,  # Number of keepalive failures before dropping connection
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that yields a database session and ensures it's properly closed.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)