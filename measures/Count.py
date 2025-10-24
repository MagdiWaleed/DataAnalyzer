from . import Measure
from models.SalesPerson import SalesPerson

class CountMeasure(Measure):
    def __init__(self):
        pass
    def countPerStage(self,data,stages=[
        "leads",
        "orphans",
        "we_called",
        "meeting",
        "gathering",
        "nda",
        "poc",
        "qualified",
        "not_qualified",
        "client_poc",
        "proposition",
        "won",
        "lost"
    ],unique =False):
        result = {
            "details":{t.name:{k:0 for k in stages} for t in data},
            "result":{k:0 for k in stages}
        }
        if unique:
            lastStages, names, companies_name = SalesPerson.getTotalLastStage(data)
        else:
            lastStages, names, companies_name= SalesPerson.getTotalCompanyLifeStages(data)
     
        companies = {
            "details":{k:[] for k in set(names)},
            "result":[]
        }
        print(len(names), len(lastStages),len(companies_name))
        
        for name, lastStage,company_name in zip(names,lastStages,companies_name):
            result['details'][name][lastStage]+=1
            result['result'][lastStage]+=1

            companies['details'][name].append({"name":company_name,"stage":lastStage})
            companies["result"].append({"name":company_name,"stage":lastStage})
        return result, companies
        

