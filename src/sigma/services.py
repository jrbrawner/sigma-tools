from sqlalchemy.orm import Session
from sigma.rule import SigmaRule
from fastapi import UploadFile

def create_sigma_rules_text(db: Session, rules_text: str):

    rule = SigmaRule.from_yaml(rules_text)
    return rules_text

def create_sigma_rules_files(db: Session, files: list[UploadFile]):

    for file in files:
        sigma_text = file.file.read().decode()
        rule = SigmaRule.from_yaml(sigma_text)
        return rule.to_dict()
        

    
