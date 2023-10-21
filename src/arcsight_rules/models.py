from sqlalchemy import Column, String
from db import Base

class ArcSightRule(Base):

    __tablename__ = "ArcSightRule"
    raw = Column(String)
    id = Column(String)
    name = Column(String)
    logic = Column(String)