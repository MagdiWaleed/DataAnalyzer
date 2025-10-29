import pandas as pd
import os

class LoadingPipeLine():
    def __init__(self,FILES_PATH = "data",sheets:int = 3):
        self.FILES_PATH = FILES_PATH
        self.sheets = sheets
        self.FILES_NAMES = os.listdir(self.FILES_PATH)

    def setFiles(self):
        dfs = []
        for path in self.FILES_NAMES: 
            file_path =  os.path.join(self.FILES_PATH,path)
            excel_file = []
            for table in [ pd.read_excel(file_path,sheet_name=f'Sheet{(t+1)}') for t in range(self.sheets)]:
                excel_file.append(table)
            dfs.append(excel_file)
        return dfs
        
    def run(self):
        dfs = self.setFiles()
        names = [t.split('reports')[0].strip() for t in self.FILES_NAMES]
        return dfs, names
    
    
if __name__ =="__main__":
    loadingPipeLine = LoadingPipeLine()
    result = loadingPipeLine.run()
        
    