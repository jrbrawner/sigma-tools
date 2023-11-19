import xml.etree.ElementTree as ET
from xml.etree.cElementTree import Element
from typing import Union
from sqlalchemy.orm import Session
import copy
import json

class Condition:

    def __init__(self):

        self.field = []
        self.operator = []
        self.variable = []

    def add_variable(self, variable):
        self.variable.append(variable)

    def add_field(self, field):
        self.field.append(field)
    
    def add_operator(self, operator):
        self.operator.append(operator)

    def reverse(self):
        """Reverse lists to preserve order when building strings."""
        self.operator.reverse()
        self.field.reverse()
        self.variable.reverse()

    def preserve_condition_metadata(self, condition_data: dict, join_condition):
        """Save condition data while still in list. Used later for constructing Sigma objects."""
        
        if condition_data.get(join_condition) is None:
            condition_data[join_condition] = [{"field" : copy.copy(self.field), "operator" : copy.copy(self.operator), "value" : copy.copy(self.variable)}]
        else:
            condition_data[join_condition].append({"field" : copy.copy(self.field), "operator" : copy.copy(self.operator), "value" : copy.copy(self.variable)})

    def create_condition_string(self):
        
        if len(self.variable) > 1 and len(self.field) > 1:
            condition_string = ""
            condition_string += f"{self.field.pop()} {self.operator.pop()} {self.variable.pop()}"
            return condition_string
        elif len(self.variable) > 1 and len(self.field) == 1:
            return f"{self.field[0]} {self.operator[0]} {self.variable}"
        else:
            return f"{self.field.pop()} {self.operator.pop()} {self.variable.pop()}"
        
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
            "attrib" : self.attrib,
            "children" : [x.serialize() for x in self.children]
        }

class ArcSightRuleXML:

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
        self.rule_type = None
        self.description_text = None

        self.sigma_metadata = {}
        self.condition_data = {}

        self.xml_conditions : Union[dict[str,str], dict[str,dict]] = None
        self.condition_list = {}
        self.condition_string : str = ""
        self.list_values : list[str] = []

        for child in self.root:

            if child.tag == "Description":
                self.__set_description(child)

            if child.tag == "Query":
                self.__set_query(child)

            if child.tag == "Actions":
                self.__set_actions(child)
        
        data = self.get_query()

        self.__set_rule_info()
        self.__get_rule_conditions(data)
        self.__assemble_condition_list()
        self.__assemble_condition_string()
        self.__assemble_metadata()
        
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
            for desc in child:
                node1 = XMLNode(
                    text=desc.text,
                    tag=desc.tag,
                    attrib=desc.attrib
                )
                for elem in desc.iter():
                    node2 = XMLNode(
                    text=elem.text,
                    tag=elem.tag,
                    attrib=elem.attrib
                )
                    node1.children.append(node2)
                del node1.children[0]
                node.children.append(node1)
            
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
            self.rule_type = self.root.attrib.get("Type")
            self.description_text = self.description.serialize().get("text")
              
    def __get_rule_conditions(self, data):

        condition_data = []
        for entry in data["query"]:
            if entry["tag"] == "WhereClause":
                for child in entry["children"]:
                    condition_data.append(child)

        self.xml_conditions = condition_data

    def __assemble_condition_list(self):

        condition_list = {}

        for condition in self.xml_conditions:
            condition_operator = None
            variable_operator = None
            
            temp = Condition()
            # enumerate condition node
            for idx, entry in enumerate(condition["children"]):
                if entry["tag"] == "BasicCondition":
                    condition_operator = entry["attrib"]["Operator"]
                    join_condition = entry["attrib"]["JoinCondition"]
                #find entry where variable text is, collect necessary information from around it
                if entry["text"] != None:
                    temp.add_variable(entry["text"])
                    if entry.get("attrib") is not None:
                        if entry.get("attrib").get("Operator") is not None:
                            variable_operator = entry["attrib"]["Operator"]
                            if variable_operator is not None:
                                temp.add_operator(variable_operator)
                            else:
                                temp.add_operator(condition_operator)
                    else:
                        temp.add_operator(condition_operator)
                        
                    if condition["children"][idx-1].get("attrib") is not None:   
                        temp.add_field(condition["children"][idx-1].get("attrib").get("Column"))
                
                #handle filter reference
                elif entry["tag"] == "Filter":
                    
                    filter_id = entry["attrib"]["ID"]
                    filter_name = entry["attrib"]["URI"].split("/").pop()
                    temp.add_variable(filter_name)
                    temp.add_operator("InFilter")
                    
                    if condition["children"][idx-1].get("attrib") is not None:   
                        temp.add_field(condition["children"][idx-1].get("attrib").get("Column"))

                #handle resource reference / active list?
                elif entry["tag"] == "Resource":

                    resource_id = entry["attrib"]["ID"]

                    resource_name = entry["attrib"]["URI"].split("/").pop()
                    temp.add_variable(resource_name)
                    temp.add_operator("InList")
                    if condition["children"][idx-1].get("attrib") is not None:   
                        temp.add_field(condition["children"][idx-1].get("attrib").get("Column"))
                        
            temp.reverse()
            #print("\n")
            if condition_list.get(join_condition) is None:
                temp.preserve_condition_metadata(self.condition_data, join_condition)
                condition_list[join_condition] = [temp.create_condition_string()]
                while len(temp.field) > 0:
                    condition_list[join_condition].append(temp.create_condition_string())
            else:
                temp.preserve_condition_metadata(self.condition_data, join_condition)
                condition_list[join_condition].append(temp.create_condition_string())

                
        self.condition_list = condition_list

    def __assemble_condition_string(self):
        condition_string = ""
        print(self.condition_list)
        for k,v in self.condition_list.items():
            if len(v) > 1:
                for idx, elem in enumerate(v):
                    condition_string += elem
                    if idx + 1 < len(v):
                        if k == "No":
                            condition_string += f" Or "
                        else:
                            condition_string += f" {k} "
            if len(v) == 1:
                if k == "No":
                    condition_string += v[0]
                    temp = list(self.condition_list) 
                    try: 
                        res = temp[temp.index(k) + 1]
                        condition_string += f" {res} " 
                    except: 
                        pass

        self.condition_string = condition_string

    def __assemble_metadata(self):

        self.sigma_metadata["detection_data"] = json.dumps(self.condition_data)
        self.sigma_metadata = json.dumps(self.sigma_metadata)

    def get_query(self) -> dict:
        return {
            "query" : [x.serialize() for x in self.query],
        }
    
    def serialize(self) -> dict:

        return {
            "name" : self.rule_name,
            "id" : self.rule_id,
            "description" : self.description_text,
            "condition_string" : self.condition_string
        }
        