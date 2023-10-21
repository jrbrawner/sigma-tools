import xml.etree.ElementTree as ET
from xml.etree.cElementTree import Element
import json
from typing import Union

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

    def __init__(self, raw):
        self.raw = raw
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
        
        list = ArcSightList(reference)

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

    def __init__(self, reference_data: dict):

        self.reference_data : dict = reference_data
        self.raw : str = None
        self.root = None

        self.list_of_lists : list[XMLNode] = None

        self.list_type : XMLNode = None
        self.entries : list[XMLNode] = None
        self.resource_id : XMLNode = None
        self.uri : XMLNode = None
        self.reference_id : XMLNode = None

        self.__get_list_xml()
        self.__parse_xml()
        self.__parse_lists()

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
                for elem in child:
                    node1 = XMLNode(
                        text=elem.text,
                        tag=elem.tag,
                        attrib=elem.attrib
                    )
                    node.children.append(node1)
            self.list_of_lists = node

    def __parse_lists(self):

        print(self.list_of_lists.serialize())
        

                
                    
                
        
        
    
        