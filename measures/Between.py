from . import Measure
from models.SalesPerson import SalesPerson
import numpy as np


class BetweenMeasure(Measure):
    def __init__(self):
        pass
    

    def stageToStage(self,salesPersons:list[SalesPerson],stage1,stage2):
        result = {
            "details":{}
        }
        total = []
        for salesPerson in salesPersons:
            days_list = salesPerson.stagesModel.stageToStage(stage1,stage2)
            total.extend(days_list)
            result['details'][salesPerson.name] = np.average(days_list) if len(days_list) >0 else 0
        
        result['result'] = np.average(total) if len(total) >0 else 0
        return result

        
    