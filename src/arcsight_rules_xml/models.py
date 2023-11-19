from sqlalchemy import Column, String, Integer
from src.db import Base

class ArcSightRule(Base):

    __tablename__ = "ArcSightRule"
    id = Column(Integer, primary_key=True)
    resource_id = Column(String)
    raw = Column(String)
    name = Column(String)
    description = Column(String)
    condition_string = Column(String)
    sigma_metadata = Column(String)

    def serialize(self):
        return {
            "resource_id" : self.resource_id,
            "name" : self.name,
            "description" : self.description,
            "condition_string" : self.condition_string,
            "raw" : self.raw
        }

