from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET
import os
from src.arcsight_rules.classes import ArcSightRule

folder_path = "test_rules"

def parse_xml_rules(db: Session):

    for file in os.listdir(folder_path):
        if ".xml" in file:
            data = open(f"{folder_path}/{file}").read()
        
    parser = ET.XMLParser(encoding="utf-8")
    root = ET.fromstring(data, parser)
    
    rule = ArcSightRule(root)

    rule.fields_being_queried()

    return rule.serialize()


        

    
