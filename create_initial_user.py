import asyncio
import os
import traceback

from dotenv import load_dotenv
from odm_p1d.connection import create_connection
from odm_p1d.collection.user import User

from app import Config

load_dotenv()


async def create_initial_user():
    mongo_session = create_connection(
        db_name=os.environ.get("MONGO_DB_NAME"),
        db_url=Config.MONGO_DB_URL
    )
    await wait_for_mongo(mongo_session)
    try:
        existing_user: None | User = await mongo_session.find_one(User, User.name == "admin")
        if existing_user:
            print("Admin user already exists.")
            return
        admin_user: User = User(
            name="admin",
            email="admin@api-p1d.com",
            password="admin123"
        )
        await mongo_session.save(admin_user)
        print("Admin user created successfully. admin admin123")
    except Exception as e:
        print(f"Error creating user {type(e).__name__}: {e}", flush=True)
        traceback.print_exc()
    finally:
        mongo_session.client.close()


async def wait_for_mongo(engine, retries=10, delay=3):
    for attempt in range(retries):
        try:
            await engine.find_one(User)
            print("MongoDB is ready.")
            return
        except Exception as e:
            print(f"Mongo not ready attempo {attempt + 1}) '{e}'.")
            await asyncio.sleep(delay)
    raise RuntimeError("Didnt connect to MongoDB.")


if __name__ == "__main__":
    asyncio.run(create_initial_user())
