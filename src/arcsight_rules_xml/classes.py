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
        self.condition_str : str = ""

        
        
        self.parse_xml_2()
        

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

    def parse_xml_2(self):

        sigma_rule = self.arcsight_xml_to_sigma(self.xml_data)

        print(sigma_rule)

    def parse_conditions(self, element):
        conditions = []
        for child in element:
            if child.tag in ['And', 'Or', 'Not']:
                nested_conditions = self.parse_conditions(child)
                if child.tag == 'Not':
                    conditions.append(f"not ({' and '.join(nested_conditions)})")
                else:
                    joiner = ' and ' if child.tag == 'And' else ' or '
                    conditions.append(f"({joiner.join(nested_conditions)})")
            elif child.tag == 'BasicCondition':
                column = child.find('.//Variable').get('Column')
                value = child.find('.//Value').text
                operator = child.get('Operator').lower()
                conditions.append(f"{column} {operator} {value}")
        return conditions
    
    def parse_basic_condition(self, basic_condition):
        """Parse a basic condition from the ArcSight XML and convert it to Sigma format."""
        operator = basic_condition.attrib['Operator']
        column = basic_condition.find('.//Variable').attrib['Column']
        value = basic_condition.find('.//Value').text

        # Map ArcSight operator to Sigma condition
        sigma_operator = {
            'GreaterThan': '>',
            'Equals': '==',
            'In': 'in',
            'NotIn': 'not in'
        }.get(operator, operator)

        return f"{column} {sigma_operator} {value}"

    def parse_condition(self, condition):
        """Parse a condition (AND, OR, NOT) from ArcSight XML and convert to Sigma format."""
        condition_type = condition.tag
        conditions = []

        for child in condition:
            if child.tag in ['And', 'Or', 'Not']:
                conditions.append(self.parse_condition(child))
            elif child.tag == 'BasicCondition':
                conditions.append(self.parse_basic_condition(child))

        if condition_type == 'And':
            return f"({') and ('.join(conditions)})"
        elif condition_type == 'Or':
            return f"({') or ('.join(conditions)})"
        elif condition_type == 'Not':
            return f"(not ({conditions[0]}))"
        else:
            return ''

    def arcsight_xml_to_sigma(self, xml_string):
        """Convert ArcSight XML rule to Sigma rule."""
        root = ET.fromstring(xml_string)
        rule_name = root.attrib['Name']

        sigma_rule = {
            'title': rule_name,
            'logsource': {
                'category': 'network'
            },
            'detection': {}
        }

        for condition in root.findall('.//Condition'):
            
            sigma_condition = self.parse_condition(condition)
            sigma_rule['detection']['condition'] = sigma_condition

        return yaml.dump(sigma_rule, sort_keys=False)
        


    


    



            
            

        
        
        
        
        
    
                
            

                
                    
         
        
        
        

        
        
            
                

        
        

                    

            

        
