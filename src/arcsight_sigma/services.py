from sqlalchemy.orm import Session
from sigma.rule import SigmaRule, SigmaLogSource, SigmaDetectionItem, SigmaDetection
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
        
def convert_arcsight_to_sigma(db: Session):

    rules = db.query(ArcSightRule).all()

    rule_list = []

    for rule in rules:
        my_rule = ArcSightToSigma(rule)
        
    
    return rule_list
