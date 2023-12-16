from sqlalchemy.orm import Session
from src.publish.classes import PublishToElasticIndex


def publish_rules_to_elasticsearch(db: Session):

    #rules = db.query(ArcSightRuleXML).all()

    helper = PublishToElasticIndex(rules, "test-sigma")

    result = helper.publish_objects()

    return result

