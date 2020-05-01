from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password


def create_table():
    Base.metadata.create_all(engine)


def create_users():
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    admin = User("admin", "admin")
    session.add(admin)

    readonly = User("readonly", "readonly")
    session.add(readonly)

    # commit the record the database
    session.commit()
