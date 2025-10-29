import streamlit as st
import datetime
import numpy as np
from PipeLines.PreProcessingPipeLine import PreProcessingTotalsPipeLine
from PipeLines.LoadingPipeLine import LoadingPipeLine
from models.TotalModel import TotalSalesPerson

loadingPipeLine = LoadingPipeLine()
preprocessing = PreProcessingTotalsPipeLine()
data,names = loadingPipeLine.run()
data = preprocessing.run(data,names)

switch = st.checkbox("Enable Filtering")

st.markdown("### Filter Range")
start_date = st.date_input("Start Date", datetime.datetime(2025, 9, 1),disabled=not switch)
end_date = st.date_input("End Date", datetime.datetime.now(),disabled=not switch)
st.divider()

if switch:
    data = TotalSalesPerson.filter_by(
                                    data,
                                   datetime.datetime.combine(start_date, datetime.time.min),
                                    datetime.datetime.combine(end_date, datetime.time.max)
                                    )
result = TotalSalesPerson.getTotalMeetings(data)
st.markdown("#### Meetings By Sales Person")
for salesPerson,value in result['details'].items():
    if salesPerson != "total":
        with st.expander("Explore "+salesPerson+" companies ("+str(len(value))+")"):
            for t in value:
                st.write(" ",t['name'],": ",t['date'])

st.markdown("#### Meetings In Total")
with st.expander("Explore The Companies ("+str(len(result['total']))+")"):
    for t in result['total']:
    
        st.write(" ",t['name'],": ",t['date'])
