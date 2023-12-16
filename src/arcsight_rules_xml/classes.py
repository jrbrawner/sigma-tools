import xmltodict
from treelib import Tree, Node

class ArcSight2Sigma:

    def __init__(self, xml_data: str):
        """Initiate a class that can be used to convert XML ArcSight rules to Python Sigma rule objects

        Args:
            xml_data (str): An ArcSight XML document in str format
        
        """
        self.xml_data = xml_data
        self.json_data = None
        self.condition_tree = Tree()

        self.convert_to_json()
        self.get_detections()

    def convert_to_json(self) -> None:
        """Convert the XML data to JSON using xmltodict library

        Args:
            None: Uses XML data passed in during class creation.
        Returns:
            None: Sets JSON data in class attribute json data.
        """
        self.json_data = xmltodict.parse(self.xml_data)

    def get_detections(self):
        
        top_condition = list(self.json_data.get("Rule").get("Condition").keys())[0]

        if top_condition is None:
            raise ValueError("Something is wrong with the XML rule format.")
        
        self.condition_tree.create_node(top_condition)
        
        for condition,subconditions in self.json_data.get("Rule").get("Condition").get(top_condition).items():
            self.parse_detections(condition, subconditions, self.condition_tree.root)

    def parse_detections(self, condition, data, parent_node):
        """Parse potential dicts and lists of condition data from ArcSight JSON rule conditions

        Args:
            Condition (str): The condition (and / or / not) which will be used as a parent node in the tree
        Returns:
            None
        """
        
        if isinstance(data, dict):
            key = (*data, )[0]
            values = data.get(key)
            for field in values:
                self.condition_tree.create_node(tag=condition, parent=condition, data=field)

         
                    

            

        
