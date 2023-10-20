import xml.etree.ElementTree as ET
from xml.etree.cElementTree import Element
import json

class ASNode:

    def __init__(self, text, tag, attrib):
        
        self.text : str = self.__process_text(text)
        self.tag : str = tag
        self.attrib : dict = self.__process_attrib(attrib)

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
            "attrib" : json.dumps(self.attrib)
        }


class ArcSightRule:

    def __init__(self, root):
        
        self.root = root

        self.description : ASNode = None
        self.query : list[ASNode] = []
        self.actions : list[ASNode] = []

        for child in root:

            if child.tag == "Description":
                self.__set_description(child)

            if child.tag == "Query":
                self.__set_query(child)

            if child.tag == "Actions":
                self.__set_actions(child)
    

    def __set_description(self, description_node : Element) -> None:

        for child in description_node.iter():
            node = ASNode(
                text=child.text,
                tag=child.tag,
                attrib=child.attrib
            )
            self.description = node

    def __set_query(self, query_node: Element) -> None:

        for child in query_node.iter():
            node = ASNode(
                text=child.text,
                tag=child.tag,
                attrib=child.attrib
            )
            
            self.query.append(node)
    
    def __set_actions(self, actions_node: Element):

        for child in actions_node.iter():
            node = ASNode(
                text=child.text,
                tag=child.tag,
                attrib=child.attrib
            )
            self.actions.append(node)

    def fields_being_queried(self):
        data = self.serialize()

        for k,v in data.items():
            if k == "query":
                for item in v:
                    print(item)

    def serialize(self) -> dict:
        return {
            "description" : self.description,
            "query" : [x.serialize() for x in self.query],
            "actions" : [x.serialize() for x in self.actions]
        }
    
        
        