import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError


from conversational_robot_pkg.database.models import Dialogue, Base


load_dotenv()
logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


engine = create_engine(
    DATABASE_URL,
    echo=False,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def init_db():

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
        print("Database initialized successfully")

    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        print("Connection error: Check DATABASE_URL and PostgreSQL status")
        raise

    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error during DB initialization: {e}")
        print(f"Database error: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error during DB initialization: {e}")
        print(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    init_db()
