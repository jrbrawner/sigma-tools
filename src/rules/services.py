from sqlalchemy.orm import Session
from sigma.rule import SigmaRule
from fastapi import UploadFile
import xml.etree.ElementTree as ET

def parse_xml(xml_file: UploadFile, db: Session):

    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(xml_file.file, parser)
    root = tree.getroot()

    for child in root:
        print(child.tag)

    return root.tag


        

    
