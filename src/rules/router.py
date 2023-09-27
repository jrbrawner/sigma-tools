from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.rules import services
from typing import Union

router = APIRouter()

@router.post("/api/parse-xml", tags=["sigma"])
def parse_xml(rules_xml: UploadFile, db: Session = Depends(get_db)):
    result = services.parse_xml(rules_xml, db)
    return result

