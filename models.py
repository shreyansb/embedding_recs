from sqlalchemy import Column, String, ARRAY, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector

engine = create_engine(
    "postgresql+psycopg2://postgres:password@localhost:5433/postgres"
)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

EMBEDDING_DIMENSIONS = 1536


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    school_name = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=False)
    instructor_names = Column(String)
    instructor_caption = Column(String)
    overview_raw = Column(String)
    personas_raw = Column(String)
    topics_raw = Column(String)
    embedding = Column(Vector(EMBEDDING_DIMENSIONS), nullable=True)
