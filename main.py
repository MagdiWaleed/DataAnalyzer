from PipeLines import PipeLine
from filters.DatesFilter import DatesFilter
from measures.Between import BetweenMeasure
import datetime
from models.SalesPerson import SalesPerson


pipeLine = PipeLine()
data = pipeLine.run()

lastStages, names = SalesPerson.getTotalCompanyLifeStages(data)
print(lastStages,names)
