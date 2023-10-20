from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.arcsight_rules import services
from typing import Union

router = APIRouter()

@router.post("/api/parse-xml-rules", tags=["arcsight"])
def parse_xml_rules(db: Session = Depends(get_db)):
    result = services.parse_xml_rules(db)
    return result

