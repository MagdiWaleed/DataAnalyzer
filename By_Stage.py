import streamlit as st
from PipeLines import PipeLine
import pandas as pd
import altair as alt
import streamlit as st
from models.SalesPerson import SalesPerson
import datetime
from datetime import timedelta
from filters.DatesFilter import DatesFilter
from measures.Count import CountMeasure
from utils.Searchers import Sheet2Searcher
# from utils.ShortCuts import DateShortCut

filter = DatesFilter()
countMeasure = CountMeasure()

if "data" not in st.session_state:
    st.warning("Upload data is required. Please go to the 'Upload Files' page.")
    st.stop()

data = st.session_state['data'] 



checkbox = st.checkbox("Show All Stages For The Company")
switch = st.checkbox("Enable Filtering")
# shortcut = st.checkbox("Show Date ShortCuts")

st.markdown("### Filter Range")
start_date = st.date_input("Start Date", ((datetime.datetime.now() - timedelta(days=7)).date()),disabled=not switch)
end_date = st.date_input("End Date", datetime.datetime.now(),disabled=not switch)
# dateShortCut = DateShortCut()



if switch:
    stages = st.multiselect(
        "Select Columns/Stages to Filter Using Them",
        options=[ 'leads','meeting',"client_poc",'we_called', 'gathering', 'nda', 'poc', 'qualified', 'won', 'lost'],
        default=[ 'leads']
    )
    data = filter(stages,data,datetime.datetime.combine(start_date, datetime.time.min),
                                       datetime.datetime.combine(end_date, datetime.time.max))

st.divider()

result,companies = countMeasure.countPerStage(data,unique=not checkbox)
# st.write(result) 
for name,salesData in result['details'].items():
    total =0
    for key,val in salesData.items():
        total+=val
    with st.expander(f"{name.capitalize()} -> Total Number of Companies: {total}"):
        df = pd.DataFrame(list(salesData.items()), columns=['Stage', 'Count'])
        st.write(df)
        if name not in companies['details'].keys():
            st.subheader("Have No Companies")
        else:
            with st.expander(f"Search By Company or Stage"):
                filter_by = st.text_input(f"Search About ... ({name})").lower()
                placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in companies['details'][name]])
                for key,value in placeholder.items():
                    st.write(f"{key}: ",value)
                st.divider()
                if len(companies['details'][name]) ==0:
                    st.subheader("Have No Companies")
                else:
                    for company in companies['details'][name]:
                        if company['name'].lower().__contains__(filter_by) or company['stage'].lower().__contains__(filter_by):
                            st.write(company['name'], " --> ",company['stage'], " --> ", st.session_state['searcher'].getModel(company['name']))


st.divider()

if checkbox:
    lastStages, names, _ = SalesPerson.getTotalCompanyLifeStages(data)
else:
    lastStages, names, _ = SalesPerson.getTotalLastStage(data)


st.write("Get total Number of Companies: ",len(SalesPerson.getTotalCompanies(data)), " Across Stages: ",len(companies['result']))

df = pd.DataFrame({
    'Salesperson': names,
    'Last Stage': lastStages
})

# Create DataFrame
temp = pd.DataFrame(list(result['result'].items()), columns=['Stage', 'Count'])

st.write(temp)

stage_counts = df['Last Stage'].value_counts().reset_index()
stage_counts.columns = ['Stage', 'Count']



chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Last Stage:N', title='Stage'),
    y=alt.Y('count():Q', title='Number of Salespeople'),
    color=alt.Color('Salesperson:N', title='Salesperson'),
    tooltip=['count():Q', 'Salesperson'],
).properties(
    title='Final Stages Distribution (Stacked by Salesperson)',
    width=800,
    height=500
)

st.altair_chart(chart, use_container_width=True)
with st.expander("Search By Company or Stage"):
    filter_by = st.text_input("Search About ... ").lower()
    placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in companies['result']])
    for key,value in placeholder.items():
        st.write(f"{key}: ",value)
    st.divider()

    for company in companies['result']:
        if company['name'].lower().__contains__(filter_by) or company['stage'].lower().__contains__(filter_by):
            st.write(company['name'], " --> ",company['stage'], " --> ",st.session_state['searcher'].getModel(company['name']))