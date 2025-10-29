from datetime import datetime

class ComparisonModel():
    def __init__(self,date:datetime):
        self.date = date
    
    def withInTheRange(self,date1,date2):
        return date1 <= self.date <= date2



class MeetingModel(ComparisonModel):
    def __init__(self, name:str, date:datetime):
        self.name = name
        super().__init__( date)


class CallsModel(ComparisonModel):
    def __init__(self, amount:int, date:datetime):
        self.amount = amount
        super().__init__( date)

class SuccessfulCallsModel(ComparisonModel):
    def __init__(self,name, date):
        self.name = name
        super().__init__(date)
    
    

class TotalModel():
    def __init__(self,meetingModels: list[MeetingModel],callsModel:list[CallsModel], successfulCalls: list[SuccessfulCallsModel]):
        self.meetingsModel = meetingModels
        self.callsModel = callsModel
        self.successfullCalls = successfulCalls
    
    def getMeetingCompanies(self):
        return [t.name for t in self.meetingsModel]
    
    def filter_by(self, starting_date, ending_date):
        filteredData =  TotalModel([],[],[])
        for t in self.meetingsModel:
            if t.withInTheRange(starting_date,ending_date):
                filteredData.meetingsModel.append(t)
        for t in self.callsModel:
            if t.withInTheRange(starting_date,ending_date):
                filteredData.callsModel.append(t)
        for t in self.successfullCalls:
            if t.withInTheRange(starting_date,ending_date):
                filteredData.successfullCalls.append(t)
        return filteredData

    

class TotalSalesPerson():
    def __init__(self,name, totalModel:TotalModel):
        self.name = name
        self.totalModel = totalModel
    
    @staticmethod
    def getTotalMeetings(totalSalesPerson:list):
        dataMap = {
            "total":[],
            "details":{}
        }
        dataMap['details'] = {t.name:[] for t in totalSalesPerson}
        
        for data in totalSalesPerson:
            temp = []
            for meetingModel in data.totalModel.meetingsModel:
                temp.append({"name": meetingModel.name, "date":meetingModel.date.date()})
            dataMap['total'].extend(temp)
            dataMap['details'][data.name] =  temp
        return dataMap

    @staticmethod
    def filter_by(totalSalesPerson:list,starting_date,ending_date):
        for t in range(len(totalSalesPerson)):
            totalSalesPerson[t].totalModel = totalSalesPerson[t].totalModel.filter_by(starting_date, ending_date)
        return totalSalesPerson

        
