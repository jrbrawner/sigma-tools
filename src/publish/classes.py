from elasticsearch import NotFoundError, ConflictError
from src.jrb.ElasticClient import ElasticClient

class PublishToElasticIndex(ElasticClient):

    def __init__(self, objects : list[object], index: str):
        """
        Can pass in any objects to this class to create / update documents in an Elastic Index.
        Objects must have a resource_id, create_es method and update_es method.
        """
        super().__init__()
        self.objects : list[object] = objects
        self.index = index

    def publish_objects(self):
        
        for rule in self.objects:
            exists = self.__check_if_rule_exists(rule.resource_id)
            if exists is None:
                self.__create_rule_document(rule)
            else:
                self.__update_rule_document(rule)
        
        return "All rules published or updated."

    def __check_if_rule_exists(self, document_id : str):
        
        try:
            result = self.client.get(index=self.index, id=document_id)
            return result
        except NotFoundError:
            result = None
            return result

    def __create_rule_document(self, rule: object):
        
        rule = rule.create_es()
        resource_id = rule.get("resource_id")
        del rule["resource_id"]
        document = rule
        try:
            self.client.create(index=self.index,
                            id=resource_id,
                            document=document)
        except ConflictError:
            print("Rule already exists!")
            pass

    def __update_rule_document(self, rule: object):
        rule = rule.update_es()
        resource_id = rule.get("resource_id")
        del rule["resource_id"]
        document = rule
        
        self.client.update(index=self.index,
                        id=resource_id,
                        doc=document)
        #print("Document updated.")

