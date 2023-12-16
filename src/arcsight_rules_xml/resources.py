from fastapi import APIRouter, Depends
from src.dependencies import get_db
import os
import xmltodict
from src.arcsight_rules_xml.classes import ArcSight2Sigma

router = APIRouter()

@router.post("/api/parse-xml-rules", tags=["arcsight"])
async def parse_xml_rules():
    
    for file in os.listdir("test_rules_xml"):
        if file == "test2.xml":
            data = open(f"test_rules_xml/{file}").read()
            converter = ArcSight2Sigma(data)
    return converter.condition_tree.to_json()
    

