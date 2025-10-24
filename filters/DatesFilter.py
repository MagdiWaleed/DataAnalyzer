from . import Filiter
from models.SalesPerson import SalesPerson
from models.StagesModel import StagesModel
import datetime

class DatesFilter(Filiter):
    def __init__(self):
        pass
    
    def filterThis(self, date, starting_date, ending_date):
        if not (date and starting_date and ending_date):
            return False 
        if isinstance(date, str):
            date = datetime.fromisoformat(date)
        if isinstance(starting_date, str):
            starting_date = datetime.fromisoformat(starting_date)
        if isinstance(ending_date, str):
            ending_date = datetime.fromisoformat(ending_date)

        return starting_date <= date <= ending_date


    
    def filter(self,salesPersons,starting_date,ending_date,stage_name):
        new_sales_persons = []

        for salePerson in salesPersons:
            new_sales_person = SalesPerson(name=salePerson.name,stagesModel=StagesModel([]))
            for company in salePerson.stagesModel.companies:
                data = company.toMap()
                if self.filterThis(data[stage_name],starting_date,ending_date):
                    new_sales_person.addCompany(company)

            new_sales_persons.append(new_sales_person)
        return new_sales_persons
    
    def __call__(self,columns, salesPersons,starting_date,ending_date):
        salesPersons = salesPersons
        
        for stage in columns:
            salesPersons = self.filter(salesPersons,starting_date,ending_date,stage)
        
        return salesPersons 


        
                