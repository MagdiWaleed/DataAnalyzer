from .LoadingPipeLine import LoadingPipeLine
from .PreProcessingPipeLine import PreProcessingPipeLine

class PipeLine():
    def __init__(self):
        self.loadingPipeLine = LoadingPipeLine()
        self.preProcessingPipeLine = PreProcessingPipeLine()
    
    def run(self):
        data,names = self.loadingPipeLine.run()
        data = self.preProcessingPipeLine.run(data, names)
        return data