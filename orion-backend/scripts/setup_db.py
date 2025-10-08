import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Check if DATABASE_URL is set
if not os.getenv('DATABASE_URL'):
    print("Error: DATABASE_URL environment variable is not set.")
    print("Please create a .env file in the project root with the following content:")
    print("\n# Database")
    print("DATABASE_URL=postgresql://postgres:postgres@localhost:5432/orion_finance\n")
    sys.exit(1)

print("Database URL found. Proceeding with migrations...")

# Run Alembic migrations
print("\nRunning database migrations...")
os.system("alembic upgrade head")

print("\nDatabase setup completed successfully!")
