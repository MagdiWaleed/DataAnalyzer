import pandas as pd

class Sheet2Searcher():
    def __init__(self,sheet2):
        self.convertToMap(sheet2)

    def convertToMap(self, sheet2):
        data = {}
        for sheet in sheet2:
            for t in sheet.iloc:
                if t["Company name"] is None or t["Model name"] is None or pd.isna(t["Model name"]) or pd.isna(t["Company name"]) :
                    continue
                data[t["Company name"]] = t["Model name"] 
        self.data = data
        self.keys = data.keys()

    def getModel(self,company_name):
        if company_name in self.keys:
            return self.data[company_name]
        else:
            return "Have No Model"
        
    def countFrequency(self,companies:list[str]):
        data = {}
        for company in companies:
            model = self.getModel(company)
            if model == "Have No Model":
                continue
            elif model not in data.keys():
                data[model]= 1 
            else:
                data[model]+=1
        return data

