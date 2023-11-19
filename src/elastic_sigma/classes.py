from src.jrb.ElasticClient import ElasticClient


class ElasticSigmaServices(ElasticClient):

    def __init__(self):
        super().__init__()
        self.index = "test-sigma"

    def query_sigma_rules(self) -> dict:

        result = self.client.search(index=self.index)
        rule_list = []
        for doc in result.get("hits").get("hits"):
            rule_list.append(doc.get("_source"))

        return rule_list
