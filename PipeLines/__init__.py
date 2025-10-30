from .LoadingPipeLine import LoadingPipeLine
from .PreProcessingPipeLine import PreProcessingPipeLine

class PipeLine():
    def __init__(self):
        self.loadingPipeLine = LoadingPipeLine()
        self.preProcessingPipeLine = PreProcessingPipeLine()
    
    def run(self,return_sheet2=False):
        data,names = self.loadingPipeLine.run()
        data,sheet2 = self.preProcessingPipeLine.run(data, names)
        if return_sheet2:
            return data, sheet2
        return data