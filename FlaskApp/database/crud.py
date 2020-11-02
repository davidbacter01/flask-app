from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
from database.config import DATABASE_URI


engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
