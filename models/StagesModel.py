from typing import List
from .Company import Company
import pandas as pd 
from datetime import  timedelta
from filters import Filiter

class StagesModel():
    def __init__(self,companies: List[Company]):
        companies = self.clearNames(companies)
        self.companies = companies
        
    
    def clearNames(self,companies):
        companies_data = []
        for t in companies:
            if pd.isna(t.name):
                continue
            companies_data.append(t)
        return companies_data
    
    # def working_days(start_date, end_date):
    #     if start_date > end_date:
    #         start_date, end_date = end_date, start_date  # swap if in wrong order

    #     total_days = 0
    #     current = start_date
    #     while current <= end_date:
    #         # weekday(): Sunday=6, Monday=0, ..., Saturday=5
    #         # Adjusting for Sunday-Thursday workweek
    #         if current.weekday() in [6, 0, 1, 2, 3]:  # Sunday(6) to Thursday(3)
    #             total_days += 1
    #         current += timedelta(days=1)
        
    #     return total_days
    
    def stageToStage(self,column1,column2):
       result = []
       companies_name = []
       stages_data = []
       for company in self.companies:
           companyMap = company.toMap()
           if companyMap[column1] is None or companyMap[column2] is None:
               continue
           name = company.name
           company = company.toMap()
           result.append(Company.working_days(company[column1],company[column2]))
           companies_name.append(name)
           stages_data.append({column1:companyMap[column1],column2:companyMap[column2]})
    
       return result, companies_name, stages_data
    
    def getLastStage(self):
        result = []
        for company in self.companies:
            result.append(company.lastStage)
        return result
       
        
    