from sqlalchemy.orm import Session
from src.elastic_sigma.classes import ElasticSigmaServices

def query_sigma_rules(db: Session): 

    helper = ElasticSigmaServices()

    rules = helper.query_sigma_rules()

    raw_rules = [x["raw"] for x in rules]

    return raw_rules




