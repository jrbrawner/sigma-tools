from elasticsearch import Elasticsearch, NotFoundError, ConflictError
from src.settings import settings
from src.arcsight_rules_xml.models import ArcSightRule

class ArcSightToElasticIndex:

    def __init__(self, arcsight_rules_xml : list[ArcSightRule]):

        self.arcsight_rules_xml : list[ArcSightRule] = arcsight_rules_xml
        self.index = "test-sigma"
        self.client = None

        self.__create_client()

    def __create_client(self):
        self.client = Elasticsearch(
            settings.ES_URL,
            api_key=settings.ES_API_KEY,
            verify_certs=False
        )

    def publish_rules(self):
        
        for rule in self.arcsight_rules_xml:

            rule = rule.serialize()
            exists = self.__check_if_rule_exists(rule.get("resource_id"))

            if exists is None:
                self.__create_rule_document(rule)
            else:
                self.__update_rule_document(rule)


    def __check_if_rule_exists(self, document_id : str):
        
        try:
            result = self.client.get(index=self.index, id=document_id)
            return result
        except NotFoundError:
            result = None
            return result

    def __create_rule_document(self, rule: dict):
        
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

    def __update_rule_document(self, rule: dict):
        resource_id = rule.get("resource_id")
        del rule["resource_id"]
        document = rule
        
        self.client.update(index=self.index,
                        id=resource_id,
                        doc=document)
        #print("Document updated.")
        

