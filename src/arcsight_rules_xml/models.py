from sqlalchemy import Column, String, Integer
from src.db import Base
from datetime import datetime

class ArcSightRuleXML(Base):

    __tablename__ = "ArcSightRuleXML"
    id = Column(Integer, primary_key=True)
    resource_id = Column(String)
    raw = Column(String)
    name = Column(String)
    description = Column(String)
    condition_string = Column(String)
    sigma_metadata = Column(String)

    def create_es(self):
        today = datetime.utcnow()
        return {
            "resource_id" : self.resource_id,
            "name" : self.name,
            "description" : self.description,
            "condition_string" : self.condition_string,
            "resource_type" : "rule",
            "original_format" : "xml",
            "date_created" : today,
            "date_updated" : None,
            "raw" : self.raw,
        }

    def update_es(self):
        today = datetime.utcnow()
        return {
            "resource_id" : self.resource_id,
            "name" : self.name,
            "description" : self.description,
            "condition_string" : self.condition_string,
            "resource_type" : "rule",
            "original_format" : "xml",
            "date_updated" : today,
            "raw" : self.raw,
        }

