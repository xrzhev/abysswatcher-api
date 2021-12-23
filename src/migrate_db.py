from sqlalchemy import create_engine

from models.hosts import Base as hosts_base
from models.certs import Base as certs_base

DB_URL = "sqlite:///db_file/abysswatcher.sqlite3"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    hosts_base.metadata.drop_all(bind=engine)
    certs_base.metadata.drop_all(bind=engine)
    hosts_base.metadata.create_all(bind=engine)
    certs_base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()