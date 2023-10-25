from sqlalchemy.orm import Session
import os
import json

def ingest_arcsight_rules(db: Session):

    folder_path = "test_rules_json"

    for file in os.listdir(folder_path):
        data = open(f"{folder_path}/{file}").read()
        rule = json.loads(data)
    
    name = rule.get("ruleName")
    description = rule.get("description")
    active = rule.get("enabled")
    conditions = rule.get("conditions")
    actions = rule.get("actions")
    
    