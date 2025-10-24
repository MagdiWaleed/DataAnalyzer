import pandas as pd
import os
from models.Company import Company
from models.SalesPerson import SalesPerson
from models.StagesModel import StagesModel
import datetime


class PreProcessingPipeLine():
    def __init__(self,columnsNames = [
       'company name',
       'Meeting', 'Orphans', 'Leads', 'We called', 'Gathering requierments',
       'NDA', 'Proof of Concept (POC)', 'Qualified', 'Not Qualified',
       'Client Approval on POC', 'Proposition', 'Won', 'Lost'
    ],default_yes_replacement =datetime.datetime(2025,9,7) ):
        self.columnsNames = columnsNames
        self.default_yes_replacement = default_yes_replacement


    def selectColumns(self,data):#->excel->sheet
        new_data = []
        for sheets in data:
            sheets[0] = sheets[0][self.columnsNames]
            new_data.append(sheets)
        return new_data
    
    
    def convertToObjectsTableStages(self, data, names):
        new_data = []
        for i, sheets in enumerate(data):
            temp = []
            for t in sheets[0].iloc:
                # Convert date columns to datetime safely
                def safe_date(val):
                    try:
                        return pd.to_datetime(val)
                    except:
                        return pd.NaT  # pandas NaT for missing/invalid dates

                company = Company(
                    name=t['company name'],
                    meeting=safe_date(t['Meeting']),
                    orphans=safe_date(t['Orphans']),
                    leads=safe_date(t['Leads']),
                    we_called=safe_date(t['We called']),
                    gathering=safe_date(t['Gathering requierments']),
                    nda=safe_date(t['NDA']),
                    poc=safe_date(t['Proof of Concept (POC)']),
                    qualified=safe_date(t['Qualified']),
                    not_qualified=safe_date(t['Not Qualified']),
                    client_poc=safe_date(t['Client Approval on POC']),
                    proposition=safe_date(t['Proposition']),
                    won=safe_date(t['Won']),
                    lost=safe_date(t['Lost']),
                    update_yes=self.default_yes_replacement
                )
                temp.append(company)

            stageModel = StagesModel(companies=temp)
            salesPerson = SalesPerson(name=names[i], stagesModel=stageModel)
            new_data.append(salesPerson)
        return new_data


    
    def run(self,data,names):
        data = self.selectColumns(data)
        salesData = self.convertToObjectsTableStages(data,names)
        return salesData
        
    