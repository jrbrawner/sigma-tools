import xmltodict
from treelib import Tree, Node
import xml.etree.ElementTree as ET

class ParseArcSightConditonsXML:

    def __init__(self, xml_data: str):
        """Initiate a class that can be used to convert XML ArcSight rules to Python Sigma rule objects

        Args:
            xml_data (str): An ArcSight XML document in str format
        
        """
        self.xml_data : str = xml_data
        self.json_data : dict = xmltodict.parse(self.xml_data)
        self.conditions : dict = self.json_data.get("Rule").get("Query").get("WhereClause").get("Condition")

        self.temp : dict = {}
        
        self.keywords = ["Not", "And", "Or"]

        self.parse_xml()
        

    def parse_xml(self):
        
        self.get_all_values(self.conditions)

    def get_all_values(self, obj, level=0):
        """Walk through a dictionary of dicts and lists."""
        if type(obj) is dict:
            for key, value in obj.items():
                if type(value) in [dict, list]:
                    print('    ' * level, key, sep='')
                    level = level + 1
                    self.get_all_values(value, level)
                    level = level - 1
                else:
                    print('    ' * (level), key, ': ', value, sep='')
        elif type(obj) is list:
            for i, element in enumerate(obj):
                if type(element) in [dict, list]:
                    print('    ' * level, i, sep='')
                    level = level + 1
                    self.get_all_values(element, level)
                    level = level - 1
                else:
                    print('    ' * (level), element, sep='')
        else:
            raise ValueError



            
            

        
        
        
        
        
    
                
            

                
                    
         
        
        
        

        
        
            
                

        
        

                    

            

        
