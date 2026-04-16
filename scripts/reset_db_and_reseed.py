import asyncio
import sys
import os

# Add the parent directory to the Python path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import AsyncSessionLocal
from scripts.seed import seed

async def reset_and_reseed():
    async with AsyncSessionLocal() as session:
        print("Clearing tables to execute fresh seeding...")
        # TRUNCATE CASCADE will wipe domains and forcefully wipe categories, companies, problems, reports, etc.
        await session.execute(text("TRUNCATE TABLE domains CASCADE;"))
        await session.commit()
        print("Tables cleared successfully. Running fresh seed...")
    
    # Run the seed function
    await seed()

if __name__ == "__main__":
    asyncio.run(reset_and_reseed())
