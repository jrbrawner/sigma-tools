from fastapi import APIRouter, Depends
from src.dependencies import get_db
import os
from src.arcsight_rules_xml.classes import ParseArcSightConditonsXML

router = APIRouter()

@router.post("/api/parse-xml-rules", tags=["arcsight"])
async def parse_xml_rules():
    
    for file in os.listdir("test_rules_xml"):
        if file == "test5adv.xml":
            data = open(f"test_rules_xml/{file}").read()
            converter = ParseArcSightConditonsXML(data)
            #converter.condition_tree.to_graphviz()
    
    return converter.json_data
    
    
    

