from abc import ABC, abstractmethod
from models.SalesPerson import SalesPerson


class Measure(ABC):
    def __init__(self):
        pass
    
    def getAllCompanies(self,salesPersons):
        companies = []
        for salesPerson in salesPersons:
            for company in salesPerson.stagesModel.companies:
                companies.append(company)
        return companies
        
    
        