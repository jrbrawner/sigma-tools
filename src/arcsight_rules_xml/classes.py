import xmltodict
from treelib import Tree, Node
import xml.etree.ElementTree as ET
import yaml
import json

class ParseArcSightConditonsXML:

    def __init__(self, xml_data: str):
        """Initiate a class that can be used to convert XML ArcSight rules to Python Sigma rule objects

        Args:
            xml_data (str): An ArcSight XML document in str format
        
        """
        self.xml_data : str = xml_data
        self.json_data : dict = xmltodict.parse(self.xml_data)
        self.conditions : dict = self.json_data.get("Rule").get("Query").get("WhereClause").get("Condition")

        self.conditions_data : dict = {}
        self.test : list = []
        
        self.parse_xml_1()
        

    def parse_xml_1(self):
        
        root = ET.fromstring(self.xml_data)

        # Extract relevant information
        rule_name = root.get('Name')
        conditions = []

        for condition in root.findall(".//BasicCondition"):
            column = condition.find('.//Variable').get('Column')
            value = condition.find('.//Value').text
            operator = condition.get('Operator')
            conditions.append({'column': column, 'value': value, 'operator': operator})

        print(conditions)
        # Prepare Sigma rule structure
        sigma_rule = {
            'title': rule_name,
            'status': 'experimental',
            'description': 'Converted from ArcSight rule',
            'logsource': {
                'product': 'network',  # Adjust this based on your environment
            },
            'detection': {
                'condition': ' and '.join(f"{c['column']} {c['operator'].lower()} {c['value']}" for c in conditions)
            },
            'falsepositives': ['Unknown'],  # Define based on your understanding
            'level': 'high'  # Set the appropriate level
        }

        # Convert to YAML format
        sigma_yaml = yaml.dump(sigma_rule, sort_keys=False)

        print(sigma_yaml)

    
        


    


    



            
            

        
        
        
        
        
    
                
            

                
                    
         
        
        
        

        
        
            
                

        
        

                    

            

        
