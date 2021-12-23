from sqlalchemy import create_engine

from models.certs import Base as certs_base

DB_URL = "sqlite:///db_file/abysswatcher.sqlite3"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    certs_base.metadata.drop_all(bind=engine)
    certs_base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
