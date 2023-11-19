from elasticsearch import Elasticsearch
from src.settings import settings

class ElasticClient:

    def __init__(self):
        self.client = None

        self.__create_client()

    def __create_client(self):
        self.client = Elasticsearch(
            settings.ES_URL,
            api_key=settings.ES_API_KEY,
            verify_certs=False
        )