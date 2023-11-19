from sqlalchemy.orm import Session
from src.publish.classes import ArcSightToElasticIndex
from src.arcsight_rules_xml.models import ArcSightRule

def publish_rules_to_elasticsearch(db: Session):

    rules = db.query(ArcSightRule).all()

    helper = ArcSightToElasticIndex(rules)

    result = helper.publish_rules()

    return result
        

