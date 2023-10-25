from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.arcsight_rules_json import services
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/api/ingest-arcsight-rules", tags=["arcsight"], response_class=JSONResponse)
def ingest_arcsight_rules(db: Session = Depends(get_db)):
    result = services.ingest_arcsight_rules(db)
    return result