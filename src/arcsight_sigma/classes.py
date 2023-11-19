from src.arcsight_rules_xml.models import ArcSightRule
from sigma.rule import SigmaRule

class ArcSightToSigma:

    def __init__(self, arcsight_rule: ArcSightRule):

        self.arcsight_rule = arcsight_rule

        self.__assemble_detection_data()

    def __assemble_detection_data(self):
        
        print(self.arcsight_rule.sigma_metadata)