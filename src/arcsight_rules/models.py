from sqlalchemy import Column, String, Integer
from src.db import Base

class ArcSightRule(Base):

    __tablename__ = "ArcSightRule"
    id = Column(Integer, primary_key=True)
    raw = Column(String)
    name = Column(String)
    logic = Column(String)

class ArcSightList(Base):

    __tablename__ = "ArcSightList"
    id = Column(Integer, primary_key=True)
    raw = Column(String)
    name = Column(String)
    list_type = Column(String)
    entries = Column(String)
    resource_id = Column(String)
    reference_id = Column(String)

    def serialize(self):
        return {
            "id" : self.id,
            "raw" : self.raw,
            "name" : self.name,
            "list_type" : self.list_type,
            "entries" : self.entries,
            "resource_id" : self.resource_id,
            "reference_id" : self.reference_id
        }

    def get_entries(self):
        return {
            "entries" : self.entries
        }

