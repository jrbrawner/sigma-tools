import xmltodict
from treelib import Tree, Node

class ConditionNode:
    
    def __init__(self, condition_list : list[list]):

        self.condition_list = condition_list
        self.keyword_list : list[str] = ["And", "Or", "Not"]

        self.keywords : list[str] = []
        self.data : list[list] = []

        self.last_keyword_index = []
        self.first_keyword : str = None
        self.last_keyword : str = None

        self.__get_keywords()
        self.__get_data()
        self.__set_last_keyword_index()

    def __get_keywords(self):
        
        for condition in self.condition_list:
            if condition in self.keyword_list:
                self.keywords.append(condition)

    def __get_data(self):
        for condition in self.condition_list:
            if condition not in self.keyword_list:
                self.data.append(condition)

    def __set_last_keyword_index(self):
        self.last_keyword_index = len(self.keywords) - 1
        self.first_keyword = self.keywords[0]
        self.last_keyword = self.keywords[self.last_keyword_index]

    def __repr__(self) -> str:
        return str(self.condition_list) 


class ConditionList:
    
    def __init__(self, generator):

        self.generator = generator
        self.generator_list = list(generator)

        self.tree : Tree = Tree()
        self.condition_list : list[ConditionNode] = []
        self.identifiers : list[ConditionNode] = []
        
        self.__get_condition_list()
        self.__build_tree()

    def __get_condition_list(self):

        #get root of conditions (generator converted 2d array)
        root = self.generator_list[0][0]
        root = self.tree.create_node(root)
        #remove root from 2d array
        [x.pop(0) for x in self.generator_list]
        
        self.condition_list = [ConditionNode(x) for x in self.generator_list]

    def __build_tree(self):

        self.identifiers = self.condition_list
       
        temp_condition = None
        ### creating a node for each new unique condition, and linking back to appropriate parent
        for item in self.condition_list:
            if item.keywords != temp_condition:
                try:
                    node = self.tree.create_node(item.last_keyword, None, item.condition_list[item.last_keyword_index-1], None)
                except:
                    node = self.tree.create_node(item.last_keyword, None, self.tree.root, None)
                for entry in self.condition_list:
                    if entry.condition_list[item.last_keyword_index] == item.last_keyword:
                        entry.condition_list[item.last_keyword_index] = node.identifier
                        
                temp_condition = item.keywords
        
        
        temp = None
        data = []
        for entry in self.condition_list:
            
            if temp != entry.condition_list[entry.last_keyword_index]:
                if len(data) > 0:
                    node = self.tree.get_node(temp)
                    node.data = str(data)
                    data.clear()
                    data.append(entry.data)
                else:
                    data.append(entry.data)
            else:
                data.append(entry.data)
            temp = entry.condition_list[entry.last_keyword_index]

        node = self.tree.get_node(temp)
        if node is not None:
            node.data = data

    

                
        


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

        condition_list = ConditionList(result)
        self.condition_tree = condition_list.tree

        s = self.condition_tree.all_nodes_itr()

        for x in s: print(x, "\n")
        

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


         
                    

            

        
