from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.arcsight_sigma import services
from typing import Union

router = APIRouter()

@router.post("/api/sigma", tags=["sigma"])
def create_sigma_rules(rules_text: str = Form(), db: Session = Depends(get_db)):
    sigma_rule_list = services.create_sigma_rules_text(db, rules_text)
    if sigma_rule_list is None:
        raise HTTPException(400, "Error in creating sigma rules.")
    return sigma_rule_list

@router.post("/api/sigma/files", tags=["sigma"])
def create_sigma_files(files: list[UploadFile], db: Session = Depends(get_db)):
    sigma_rule_list = services.create_sigma_rules_files(db, files)
    if sigma_rule_list is None:
        raise HTTPException(400,"Error in creating sigma rules.")
    return sigma_rule_list

@router.post("/api/convert-arcsight-to-sigma", tags=['sigma'])
def convert_arcsight_to_sigma(files: list[UploadFile], db: Session = Depends(get_db)):
    result = services.convert_arcsight_to_sigma(db, files)
    return result

