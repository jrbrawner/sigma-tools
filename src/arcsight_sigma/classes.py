from src.arcsight_rules_xml.models import ArcSightRule
from sigma.rule import SigmaRule, SigmaDetections, SigmaDetection, SigmaDetectionItem, SigmaLogSource
from sigma.modifiers import SigmaContainsModifier, SigmaCompareModifier, SigmaExistsModifier, SigmaAllModifier
from sigma.conditions import ConditionAND, ConditionOR, ConditionNOT
from sigma.types import SigmaString
import json

class ArcSightToSigma:

    def __init__(self, arcsight_rule: ArcSightRule):

        self.arcsight_rule = arcsight_rule
        self.arcsight_rule.sigma_metadata = json.loads(self.arcsight_rule.sigma_metadata)

        self.sigma_rule = None

        self.__assemble_detection_data()

    def __assemble_detection_data(self):
        
        detection_data = json.loads(self.arcsight_rule.sigma_metadata.get("detection_data"))

        detection_items = []
        detections = []

        for k,v in detection_data.items():
            if len(v) > 1:
                for entry in v:
                    for k,v in entry.items():
                        if k == "field":
                            field = v[0]
                        if k == "operator":
                            operator = v[0]
                        if k == "value":
                            if len(v) > 1:
                                variable = v
                            else:
                                variable = v[0]
                    mods = []

                    detection_item = SigmaDetectionItem(field=field, modifiers=mods, value=variable)
                    #detection_items.append(detection_item)
                    detection = SigmaDetection([detection_item])
                    detections.append(detection)
            else:
                for k,v in v[0].items():
                    
                    if k == "field":
                        field = v[0]
                    if k == "operator":
                        operator = v[0]
                    if k == "value":
                        if len(v) > 1:
                            variable = v
                        else:
                            variable = v[0]
                mods = []

                detection_item = SigmaDetectionItem(field=field, modifiers=mods, value=variable)
                #detection_items.append(detection_item)
        
                detection = SigmaDetection([detection_item])
                detections.append(detection)
        
        detection_list = {}
        for idx, entry in enumerate(detections):
            detection_list[f"selection{idx}"] = entry
        
        conditions = list(detection_list.keys())

        detections = SigmaDetections(detections=detection_list, condition=conditions)

        source = SigmaLogSource("vendor", "test")

        rule = SigmaRule(title=self.arcsight_rule.name,
                         description=self.arcsight_rule.description,
                         logsource=source,
                         detection=detections)
        
        self.sigma_rule = rule

        
        
        

        

