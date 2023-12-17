import xmltodict
from treelib import Tree, Node
from collections import abc
from collections.abc import Iterator

class ArcSight2Sigma:

    def __init__(self, xml_data: str):
        """Initiate a class that can be used to convert XML ArcSight rules to Python Sigma rule objects

        Args:
            xml_data (str): An ArcSight XML document in str format
        
        """
        self.xml_data = xml_data
        self.json_data = None
        self.condition_tree : Tree = Tree()

        self.convert_to_json()
        self.create_condition_tree()
        
        

    def convert_to_json(self) -> None:
        """Convert the XML data to JSON using xmltodict library

        Args:
            None: Uses XML data passed in during class creation.
        Returns:
            None: Sets JSON data in class attribute json data.
        """
        self.json_data = xmltodict.parse(self.xml_data)

    def create_condition_tree(self) -> None:
        """Convert the JSON conditions into a tree

        Args:
            None: Uses JSON data in class attribute json data.
        Returns:
            None: Builds tree of JSON detection data. Root node is top condition with child nodes of the different unique conditions.
        """
        
        result = self.dict_generator(self.json_data.get("Rule").get("Condition"))
        result = list(result)
        keywords = ["And", "Or", "Not"]

        #get root of conditions (generator converted 2d array)
        root = result[0][0]
        root = self.condition_tree.create_node(root)
        #remove root from 2d array
        [x.pop(0) for x in result]
        conditions = []

        for entry in result:
            counter = 0
            for item in entry:
                if item in keywords:
                    counter += 1
                elif item not in keywords:
                    conditions.append(entry[0:counter])
                    break
                else:
                    pass
        
        
        
        


    def iter_condition_tree(self, condition, data, parent_node):
        """Enumerate all of the root node children and expand them into subsequent child nodes as necessary.
        Args:
            None: Uses condition tree
        Returns:
            None
        """

    def dict_generator(self, indict, pre=None):
        pre = pre[:] if pre else []
        if isinstance(indict, dict):
            for key, value in indict.items():
                if isinstance(value, dict):
                    for d in self.dict_generator(value, pre + [key]):
                        yield d
                elif isinstance(value, list) or isinstance(value, tuple):
                    for v in value:
                        for d in self.dict_generator(v, pre + [key]):
                            yield d
                else:
                    yield pre + [key, value]
        else:
            yield pre + [indict]


         
                    

            

        
