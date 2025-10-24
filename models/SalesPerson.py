from .StagesModel import StagesModel
from typing import List

class SalesPerson():
    def __init__(self,name:str,stagesModel:StagesModel):
        self.name = name
        self.stagesModel = stagesModel
    
    def addCompany(self,company):
        self.stagesModel.companies.append(company)

    @staticmethod
    def getTotalCompanies(salesPersons):
        companies = []
        for salesPerson in salesPersons:
            companies.extend(salesPerson.stagesModel.companies)
        return companies
   
    @staticmethod
    def getTotalLastStage(salesPersons):
        companies_name = []
        lastStage = []
        salesPersonsNames = []
        for salesPerson in salesPersons:
            for company in salesPerson.stagesModel.companies:
                companies_name.append(company.name)
                lastStage.append(company.lastStage)
                salesPersonsNames.append(salesPerson.name)
        return lastStage, salesPersonsNames,companies_name
    
    @staticmethod
    def getTotalCompanyLifeStages(salesPersons):
        companies_name = []
        stages = []
        salesPersonsNames = []
        for salesPerson in salesPersons:
            for company in salesPerson.stagesModel.companies:
                for stage in company.getLifeStages():
                    companies_name.append(company.name)
                    stages.append(stage)
                    salesPersonsNames.append(salesPerson.name)
        return stages, salesPersonsNames, companies_name
    


    
