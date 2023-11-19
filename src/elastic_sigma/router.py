from fastapi import APIRouter, Depends
from src.dependencies import get_db
from src.elastic_sigma import services
from sqlalchemy.orm import Session
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/api/query-sigma-rules", tags=["elastic"])
def query_sigma_rules(db: Session = Depends(get_db)):
    result = services.query_sigma_rules(db)
    return result