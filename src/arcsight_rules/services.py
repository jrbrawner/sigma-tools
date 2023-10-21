from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET
import os
from src.arcsight_rules.classes import ArcSightRule

folder_path = "test_rules"

def parse_xml_rules(db: Session):
    
    rule_list = []

    for file in os.listdir(folder_path):
        if ".xml" in file and "test" in file:
            data = open(f"{folder_path}/{file}", encoding="utf-8").read()
            
            rule = ArcSightRule(data)
            rule_list.append(rule)
            

    return [x.parsed_serialize() for x in rule_list]


        

    
