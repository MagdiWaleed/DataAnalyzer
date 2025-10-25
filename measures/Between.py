from . import Measure
from models.SalesPerson import SalesPerson
import numpy as np


class BetweenMeasure(Measure):
    def __init__(self):
        pass
    

    def stageToStage(self,salesPersons:list[SalesPerson],stage1,stage2):
        result = {
            "details":{}
            ,
            "result":{
                "companies":[],
                "average":0,
            }
        }
        result['details'] = {t.name:{
                    "companies":[],
                    "average":0,
                } for t in salesPersons}
        
        total_companies_name = []
        total = []
        for salesPerson in salesPersons:
            days_list, companies_name= salesPerson.stagesModel.stageToStage(stage1,stage2)
            total.extend(days_list)
            total_companies_name.extend(companies_name)
            result['details'][salesPerson.name]['average'] = np.average(days_list) if len(days_list) >0 else 0
            companies =  [{"name":companies_name[t], "days":days_list[t]} for t in range(len(days_list))]
            companies = np.array(companies)
            indcies = np.argsort(days_list)[::-1]
            companies = companies[indcies]
            companies = companies.tolist()

            result['details'][salesPerson.name]['companies'] = companies
            
        indcies = np.argsort(total)[::-1]
        companies = np.array([{"name":total_companies_name[t],"days":total[t]} for t in range(len(total_companies_name))])
        companies =companies[indcies]
        companies =companies.tolist()

        result["result"]['companies']= companies

        result['result']['average'] = np.average(total) if len(total) >0 else 0
        return result

        
    