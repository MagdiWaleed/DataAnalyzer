import pandas as pd
import os

class LoadingPipeLine():
    def __init__(self,FILES_PATH = "data",sheets:int = 3, uploaded_files=None, names=None):
        self.FILES_PATH = FILES_PATH
        self.sheets = sheets
        self.uploaded_files = uploaded_files
        self.given_names = names
        
        if self.uploaded_files is None:
            self.FILES_NAMES = os.listdir(self.FILES_PATH)
        else:
            self.FILES_NAMES = []

    def setFiles(self):
        dfs = []
        if self.uploaded_files:
            for file_obj in self.uploaded_files:
                excel_file = []
                for t in range(self.sheets):
                    file_obj.seek(0)
                    excel_file.append(pd.read_excel(file_obj,sheet_name=f'Sheet{(t+1)}'))
                dfs.append(excel_file)
        else:
            for path in self.FILES_NAMES: 
                file_path =  os.path.join(self.FILES_PATH,path)
                excel_file = []
                for table in [ pd.read_excel(file_path,sheet_name=f'Sheet{(t+1)}') for t in range(self.sheets)]:
                    excel_file.append(table)
                dfs.append(excel_file)
        return dfs
        
    def run(self):
        dfs = self.setFiles()
        if self.uploaded_files and self.given_names:
            names = self.given_names
        else:
            names = [t.split('reports')[0].strip() for t in self.FILES_NAMES]
        return dfs, names
    
    
if __name__ =="__main__":
    loadingPipeLine = LoadingPipeLine()
    result = loadingPipeLine.run()
        
    