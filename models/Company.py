from datetime import datetime, timedelta
import pandas as pd

class Company():
    def __init__(self,
                  name,
                  meeting,
                  orphans,
                  leads,
                  we_called,
                  gathering,
                  nda,poc,
                  qualified,
                  not_qualified,
                  client_poc,
                  proposition,won,
                  lost,
                  update_yes
                 ):
        self.name = name
        self.meeting = meeting
        self.orphans = orphans
        self.leads = leads
        self.we_called = we_called
        self.gathering = gathering
        self.nda = nda
        self.poc = poc
        self.qualified = qualified
        self.not_qualified = not_qualified
        self.client_poc = client_poc
        self.proposition = proposition
        self.won = won
        self.lost = lost
        self.update_yes = update_yes
        self.updateYes()
        self.map = {
            "leads": self.leads,
            "orphans": self.orphans,
            "we_called": self.we_called,
            "meeting": self.meeting,
            "gathering": self.gathering,
            "nda": self.nda,
            "poc": self.poc,
            "qualified": self.qualified,
            "not_qualified": self.not_qualified,
            "client_poc": self.client_poc,
            "proposition": self.proposition,
            "won": self.won,
            "lost": self.lost
        }
        
        valid_dates = {k: v for k, v in self.map.items() if v is not None}

        if valid_dates:
            stage_order = {stage: i for i, stage in enumerate(self.map.keys())}
            
            self.lastStage = max(
                valid_dates,
                key=lambda k: (valid_dates[k], stage_order[k])  
            )
            
            self.lastStageDate = valid_dates[self.lastStage]
        else:
            self.lastStage = None
            self.lastStageDate = None

    
    def updateYes(self):
        if isinstance(self.meeting,str):
            self.meeting = self.update_yes
        elif  pd.isna(self.meeting):
            self.meeting = None  

        if isinstance(self.orphans,str):
            self.orphans = self.update_yes
        elif  pd.isna(self.orphans):
            self.orphans = None  

        if isinstance(self.leads,str):
            self.leads = self.update_yes
        elif  pd.isna(self.leads):
            self.leads = None  

        if isinstance(self.we_called,str):
            self.we_called = self.update_yes
        elif  pd.isna(self.we_called):
            self.we_called = None  

        if isinstance(self.gathering,str):
            self.gathering = self.update_yes
        elif  pd.isna(self.gathering):
            self.gathering = None  

        if isinstance(self.nda,str):
            self.nda = self.update_yes
        elif  pd.isna(self.nda):
            self.nda = None  

        if isinstance(self.poc,str):
            self.poc = self.update_yes
        elif  pd.isna(self.poc):
            self.poc = None  

        if isinstance(self.qualified,str):
            self.qualified = self.update_yes
        elif  pd.isna(self.qualified):
            self.qualified = None  

        if isinstance(self.not_qualified,str):
            self.not_qualified = self.update_yes
        elif  pd.isna(self.not_qualified):
            self.not_qualified = None  

        if isinstance(self.client_poc,str):
            self.client_poc = self.update_yes
        elif  pd.isna(self.client_poc):
            self.client_poc = None  

        if isinstance(self.proposition,str):
            self.proposition = self.update_yes
        elif  pd.isna(self.proposition):
            self.proposition = None  

        if isinstance(self.won,str):
            self.won = self.update_yes
        elif  pd.isna(self.won):
            self.won = None  

        if isinstance(self.lost,str):
            self.lost = self.update_yes
        elif  pd.isna(self.lost):
            self.lost = None  

    def toMap(self):
        return self.map
    
    def getLifeStages(self):
        valid_dates = [k for k, v in self.map.items() if v is not None]
        return valid_dates
         


    
    @staticmethod
    def working_days(start_date, end_date):
        if start_date > end_date:
            start_date, end_date = end_date, start_date  # swap if in wrong order

        total_days = 0
        current = start_date
        while current < end_date:
            
            # weekday(): Sunday=6, Monday=0, ..., Saturday=5
            # Adjusting for Sunday-Thursday workweek
            if current.weekday() in [6, 0, 1, 2, 3]:  # Sunday(6) to Thursday(3)
                total_days += 1
            current += timedelta(days=1)
        
        return total_days
    

    
    
    
    