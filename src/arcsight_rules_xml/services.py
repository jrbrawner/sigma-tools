from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET
import os
from src.arcsight_rules_xml.classes import ArcSightRuleXML
from src.arcsight_rules_xml.models import ArcSightRuleXML as _ArcSightRuleXML

folder_path = "test_rules"

def parse_xml_rules(db: Session):
    
    rule_list = []

    for file in os.listdir(folder_path):
        if ".xml" in file and "test" in file:
            data = open(f"{folder_path}/{file}", encoding="utf-8").read()
            rule = ArcSightRuleXML(data, db)

            

            if db.query(_ArcSightRuleXML).filter(_ArcSightRuleXML.resource_id == rule.rule_id).first() is None:
                db_rule = _ArcSightRuleXML(
                    resource_id=rule.rule_id,
                    raw=rule.raw,
                    name=rule.rule_name,
                    description=rule.description_text,
                    condition_string=rule.condition_string,
                    sigma_metadata=rule.sigma_metadata                
                )
                db.add(db_rule)
            rule_list.append(rule)

    db.commit()
            

    return [x.serialize() for x in rule_list]


        

    
