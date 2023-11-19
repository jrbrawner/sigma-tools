from sqlalchemy.orm import Session
from sigma.rule import SigmaRule
from fastapi import UploadFile
from src.arcsight_rules_xml.models import ArcSightRule
from src.arcsight_sigma.classes import ArcSightToSigma

def create_sigma_rules_text(db: Session, rules_text: str):

    rule = SigmaRule.from_yaml(rules_text)
    return rules_text

def create_sigma_rules_files(db: Session, files: list[UploadFile]):

    for file in files:
        sigma_text = file.file.read().decode()
        rule = SigmaRule.from_yaml(sigma_text)

        print(rule.detection.to_dict())

        return rule.to_dict()
        
def convert_arcsight_to_sigma(db: Session, files: list[UploadFile]):

    for file in files:
            sigma_text = file.file.read().decode()
            rule = SigmaRule.from_yaml(sigma_text)

            print(rule.detection.to_dict())
            print("\n")

    rules = db.query(ArcSightRule).all()

    rule_list = []
    
    
    my_rule = ArcSightToSigma(rules[0])
        
    
    return my_rule.sigma_rule.to_dict()
