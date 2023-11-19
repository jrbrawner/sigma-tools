from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.publish import services
from typing import Union

router = APIRouter()

@router.post("/api/publish/rules-elasticsearch", tags=["publish"])
def publish_rules_to_elasticsearch(db: Session = Depends(get_db)):
    result = services.publish_rules_to_elasticsearch(db)
    return result