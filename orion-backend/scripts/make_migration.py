import os
import sys
import argparse
from dotenv import load_dotenv
from pathlib import Path

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Create a new database migration.')
    parser.add_argument('message', help='A short description of the migration')
    args = parser.parse_args()
    
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
    
    # Run Alembic to create a new migration
    print(f"Creating new migration: {args.message}")
    os.system(f'alembic revision --autogenerate -m "{args.message}"')
    
    print("\nMigration created. Don't forget to review and test it before applying!")
    print("To apply the migration, run: python -m scripts.setup_db")

if __name__ == "__main__":
    main()
