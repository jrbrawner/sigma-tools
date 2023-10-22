import xml.etree.ElementTree as ET
from xml.etree.cElementTree import Element
import json
from typing import Union
from sqlalchemy.orm import Session
from src.arcsight_rules.models import ArcSightRule as _ArcSightRule, ArcSightList as _ArcSightList

class XMLNode:

    def __init__(self, text, tag, attrib):
        
        self.text : str = self.__process_text(text)
        self.tag : str = tag
        self.attrib : dict = self.__process_attrib(attrib)
        self.children : list[XMLNode] = []

    def __process_text(self, text: str) -> None | str:

        if text == None:
            return None
        if text.strip() == "":
            return None
        return text.strip()

    def __process_attrib(self, attrib: dict) -> None | str:
        if len(attrib) == 0:
            return None
        else:
            return attrib
        
    def serialize(self) -> dict:
        return {
            "text" : self.text,
            "tag" : self.tag,
            "attrib" : json.dumps(self.attrib),
            "children" : [x.serialize() for x in self.children]
        }


class ArcSightRule:

    def __init__(self, raw, db: Session):
        self.raw = raw
        self.db = db
        parser = ET.XMLParser(encoding="utf-8")
        self.root = ET.fromstring(self.raw, parser)

        self.description : XMLNode = None
        self.query : list[XMLNode] = []
        self.actions : list[XMLNode] = []
        
        self.rule_name = None
        self.rule_id = None
        self.logic : Union[dict[str,str], dict[str,dict]] = None

        for child in self.root:

            if child.tag == "Description":
                self.__set_description(child)

            if child.tag == "Query":
                self.__set_query(child)

            if child.tag == "Actions":
                self.__set_actions(child)
        
        data = self.serialize()

        self.__set_rule_info()
        self.__fields_being_queried(data)
        self.__get_dependencies()
    

    def __set_description(self, description_node : Element) -> None:

        for child in description_node.iter():
            node = XMLNode(
                text=child.text,
                tag=child.tag,
                attrib=child.attrib
            )
            self.description = node

    def __set_query(self, query_node: Element) -> None:

        for child in query_node:
            node = XMLNode(
                text=child.text,
                tag=child.tag,
                attrib=child.attrib
            )
                
            for elem in child.iter():
                node1 = XMLNode(
                    text=elem.text,
                    tag=elem.tag,
                    attrib=elem.attrib
                )
                node.children.append(node1)
            del node.children[0]
            self.query.append(node)

    def __set_actions(self, actions_node: Element):

        for child in actions_node.iter():
            node = XMLNode(
                text=child.text,
                tag=child.tag,
                attrib=child.attrib
            )
            self.actions.append(node)

    def __set_rule_info(self):
        
        if self.root.tag == "Rule":
            self.rule_id = self.root.attrib["ID"]
            self.rule_name = self.root.attrib["Name"]
            

    def __fields_being_queried(self, data):
        
        fields_values = {}

        for idx, elem in enumerate(data["query"]):
            if elem["tag"] == "WhereClause":
                for idx, entry in enumerate(elem["children"]):
                    if entry["tag"] == "Variable":
                        if elem["children"][idx+1]["text"] is not None:
                            #print(json.loads(entry["attrib"]).get("Column"), elem["children"][idx+1]["text"])
                            fields_values[json.loads(entry["attrib"]).get("Column")] = elem["children"][idx+1]["text"]
                        elif elem["children"][idx+1]["tag"] == "Resource":
                            #print(json.loads(entry["attrib"]).get("Column"), elem["children"][idx+1])
                            fields_values[json.loads(entry["attrib"]).get("Column")] = elem["children"][idx+1]["attrib"]
        self.logic = fields_values          

    def __get_dependencies(self):
        
        for field, value in self.logic.items():
            test = json.loads(value)
            if type(test) == dict:
                if "List" in test.get("URI"):
                    self.__get_list(test)
                if "Filter" in test.get("URI"):
                    pass
                
    def __get_list(self, reference: dict):
        
        
        list = XMLList(reference, self.db)

        list = self.db.query(_ArcSightList).filter(_ArcSightList.resource_id == reference.get("ID")).first()
        
        for k,v in list.get_entries().items():
            for entry in json.loads(v):
                print(entry)

    def serialize(self) -> dict:
        return {
            "description" : self.description,
            "query" : [x.serialize() for x in self.query],
            "actions" : [x.serialize() for x in self.actions]
        }
    
    def parsed_serialize(self) -> dict:
        return {
            "name" : self.rule_name,
            "id" : self.rule_id,
            "logic" : self.logic
        }
    

class ArcSightList:

    def __init__(self, raw: str, name: str, list_type: str, entries: list[dict], resource_id: str, uri: str, reference_id: str):
        self.raw = raw
        self.name = name
        self.list_type = list_type
        self.entries = entries
        self.resource_id = resource_id
        self.uri = uri
        self.reference_id = reference_id


class XMLList:

    def __init__(self, reference_data: dict, db: Session):

        self.reference_data : dict = reference_data
        self.db = db
        self.raw : str = None
        self.root = None

        self.list_of_XML_lists : list[XMLNode] = []
        self.list_of_AS_lists : list[ArcSightList] = []

        self.name : str = None
        self.list_type : str = None
        self.entries : list[dict] = []
        self.resource_id : XMLNode = None
        self.uri : XMLNode = None
        self.reference_id : XMLNode = None

        self.__get_list_xml()
        self.__parse_xml()
        self.__parse_lists()
        self.__save_in_database()

    def __get_list_xml(self):

        ### PROBABLY AN API CALL HERE

        self.raw = open(f"test_rules\list.xml", encoding="utf-8").read()
        parser = ET.XMLParser(encoding="utf-8")
        self.root = ET.fromstring(self.raw, parser)

        ###

        
    def __parse_xml(self):
        if "lists" in self.root.tag:
            for child in self.root:
                node = XMLNode(
                    text=child.text,
                    tag=child.tag,
                    attrib=child.attrib
                )
                for elem in child.iter():
                    node1 = XMLNode(
                        text=elem.text,
                        tag=elem.tag,
                        attrib=elem.attrib
                    )
                    node.children.append(node1)
                del node.children[0]            
                self.list_of_XML_lists.append(node)

    def __parse_lists(self):

        lists = [x.serialize() for x in self.list_of_XML_lists]

        for list in lists:
            name = json.loads(list["attrib"])["name"]

            for item in list["children"]:
                if item["tag"] == "listType":
                    list_type = item["text"]
                
                if item["tag"] == "entry":
                    self.entries.append(item["attrib"])
                
                if item["tag"] == "resourceID":
                    self.resource_id = item["text"]
                
                if item["tag"] == "uri":
                    self.uri = item["text"]
                
                if item["tag"] == "referenceID":
                    self.reference_id = item["text"]

            list = ArcSightList(
                raw=self.raw,
                name=name,
                list_type=list_type,
                entries=self.entries,
                resource_id=self.resource_id,
                uri=self.uri,
                reference_id=self.reference_id
            )
            self.list_of_AS_lists.append(list)
            name = None
            list_type = None
            self.entries = None
            self.resource_id = None
            self.uri = None
            self.reference_id = None
            
    def __save_in_database(self):

        for list in self.list_of_AS_lists:

            if self.db.query(_ArcSightList).filter(_ArcSightList.resource_id == list.resource_id).first() is None:

                db_list = _ArcSightList(
                    raw=self.raw,
                    name=list.name,
                    list_type=list.list_type,
                    entries=json.dumps(list.entries),
                    resource_id=list.resource_id,
                    reference_id=list.reference_id
                )
                self.db.add(db_list)
                self.db.commit()

    def return_list(self):

        for list in self.list_of_AS_lists:
            if self.reference_data.get("ID") == list.resource_id:
                return list
            


        
            
            
                


        

                
                    
                
        
        
    
        