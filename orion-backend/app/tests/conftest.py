import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set dummy environment variables before importing the app
# These are required for the settings to be loaded correctly
os.environ["TESTING"] = "True"
os.environ["VITE_SUPABASE_URL"] = "http://test-supabase-url.com"
os.environ["VITE_SUPABASE_PUBLISHABLE_KEY"] = "test-supabase-key"
os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/testdb"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"


from app.core.database import Base
from app.dependencies import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def db_engine():
    """
    Fixture for a database engine.
    """
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Fixture for a database session.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Fixture for a test client.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

    del app.dependency_overrides[get_db]