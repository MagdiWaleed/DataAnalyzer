import pandas as pd
import os
from models.Company import Company
from models.SalesPerson import SalesPerson
from models.StagesModel import StagesModel
import datetime
from models.TotalModel import (
    TotalModel,
    SuccessfulCallsModel,
    MeetingModel,
    CallsModel,
    TotalSalesPerson
    )

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
    
        
class PreProcessingTotalsPipeLine():# total calls / meetings
    def __init__(self):
        self.update = datetime.datetime(2025,9,7)
    def extractTables(self,data):
        stages = []
        meetingTable = []
        callsTable = []
        for sheets in data:
            stage = sheets[0][["company name","Meeting",'We called']]
            # sheets[2] = sheets[2][['Company Name','Meeting Date','Number of Calles', "calls Date"]]
            # print(sheets[2])
            meetingTable.append(sheets[2][['Company Name','Meeting Date']])
            callsTable.append( sheets[2][['Number of Calles', "Calls Date"]])
            stages.append(stage)
        return stages,meetingTable,callsTable
    
    def isValid(self,meeting:MeetingModel, data:list[MeetingModel],index:int)-> bool:
        for tt in range(index+1,len(data)):
            if meeting.name == data[tt].name:
                return False
        return True
    
    def run(self,data,names):
        stages,meetingTable,callsTable = self.extractTables(data)
        new_data = []
        
        for t in range(len(stages)):
            meetings = []
            successfulCalls = []
            total_calls = []
            for tt in stages[t].iloc:
                if isinstance(tt['Meeting'],str):
                    tt['Meeting'] = self.update
                elif not  pd.isna(tt['Meeting']):           
                    meetings.append(MeetingModel(tt['company name'],tt['Meeting']))
            
            for tt in stages[t].iloc:
                if isinstance(tt['We called'],str):
                    tt['We called'] = self.update
                elif not  pd.isna(tt['We called']):
                    successfulCalls.append(SuccessfulCallsModel(tt['company name'],tt['We called']))
        
            for  tt in meetingTable[t].iloc:
                if isinstance(tt['Meeting Date'],str):
                    tt['Meeting Date'] = self.update
                elif not  pd.isna(tt['Meeting Date']):
                    meetings.append(MeetingModel(tt['Company Name'],tt['Meeting Date']))
         
            for  tt in callsTable[t].iloc:
                if isinstance(tt['Calls Date'],str):
                    tt['Calls Date'] = self.update
                elif not  pd.isna(tt['Calls Date']):
                    total_calls.append(CallsModel(tt['Number of Calles'],tt['Calls Date']))
         
            totalModel =TotalModel(meetingModels= [t for i,t in enumerate(meetings) if self.isValid(t,meetings,i)],callsModel=list(set(total_calls)),successfulCalls=list(set(successfulCalls)))
            totalSalesPerson = TotalSalesPerson(name=names[t],totalModel=totalModel)
            new_data.append(totalSalesPerson)
        return new_data

    
    
        

