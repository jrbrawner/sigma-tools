from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.arcsight_rules_xml import services
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/api/parse-xml-rules", tags=["arcsight"], response_class=JSONResponse)
def parse_xml_rules(db: Session = Depends(get_db)):
    result = services.parse_xml_rules(db)
    return result

