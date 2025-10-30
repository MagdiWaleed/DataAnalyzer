import streamlit as st
import datetime
import numpy as np
from PipeLines import PipeLine
from filters.DatesFilter import DatesFilter
from measures.Between import BetweenMeasure
from models.SalesPerson import SalesPerson
import pandas as pd
import altair as alt
from measures.Count import CountMeasure
from datetime import timedelta
from utils.Searchers import Sheet2Searcher


st.set_page_config(
    page_title="Stage Comparison Dashboard",
    layout="wide"
    
)

st.title("📊 Stage-to-Stage Comparison")


if "data" not in st.session_state.keys():
    pipeLine = PipeLine()
    data, sheet2 = pipeLine.run(return_sheet2=True)
    st.session_state['searcher'] = Sheet2Searcher(sheet2)
    st.session_state['data'] = data

data = st.session_state['data'] 


col1,col2,col3 = st.columns([1,1,1])
with col1:
    st.markdown("### Stages")
    stage1 = st.multiselect(
        "Select Columns/Stages to Compare",
        options=[ 'leads','we_called', 'gathering', 'nda', 'poc', 'qualified', 'won', 'lost'],
        default=[ 'leads'],
        max_selections=1
    )
    stage2 = st.multiselect(
        "Select Columns/Stages to Compare",
        options=[ 'leads','we_called', 'gathering', 'nda', 'poc', 'qualified', 'won', 'lost'],
        default=[ 'we_called'],
        max_selections=1
    )
with col2:
    st.markdown("### Date Range 1")
    start_date1 = st.date_input("Start Date 1", datetime.datetime.now().date() - timedelta(days=7+4))
    end_date1 = st.date_input("End Date 1", datetime.datetime.now().date()- timedelta(days=7))

with col3:
    st.markdown("### Date Range 2")
    start_date2 = st.date_input("Start Date 2", datetime.datetime.now().date() - timedelta(days=4))
    end_date2 = st.date_input("End Date 2", datetime.datetime.now().date() )

filter_based_on = st.selectbox("Filter Based On",["Both",stage1[0],stage2[0]])

st.divider()
# try:
stage1 = stage1[0]
stage2 = stage2[0]
st.markdown(f"> 0 Means The Company Goes from {stage1.capitalize()} to {stage2.capitalize()} at the same Day")
st.divider()



if filter_based_on =="Both":
    filter_by = [stage1,stage2]
elif filter_based_on == stage1:
    filter_by = [stage1] 
elif filter_based_on == stage2:
    filter_by = [stage2] 


filter1 = DatesFilter()
filtered_data1 = filter1(filter_by,data, datetime.datetime.combine(start_date1, datetime.time.min),
                                    datetime.datetime.combine(end_date1, datetime.time.max))

filter2 = DatesFilter()
filtered_data2 = filter2(filter_by,data, datetime.datetime.combine(start_date2, datetime.time.min),
                                    datetime.datetime.combine(end_date2, datetime.time.max))


measure = BetweenMeasure()

st.subheader("Date Range 1")
result1 = measure.stageToStage(filtered_data1, stage1,stage2)
result2 = measure.stageToStage(filtered_data2, stage1,stage2)
# st.write(len(filtered_data1[index].stagesModel.companies))
# st.write(result1)



def showSalesPersonData(result,key,value):
    st.subheader(key.capitalize())
    st.write("Number of Companies: ",len(result["details"][key]['companies'])," With in this range")
    if len(result["details"][key]['companies']) >0:
        st.write("Average days between the 2 Stages: ",value['average'])
        st.write("Max Waiting Days: ",result["details"][key]['companies'][0]['days'])
        st.write("Min Waiting Days: ",result["details"][key]['companies'][-1]['days'])
    else:
        st.subheader("Have No Companies")
    numberOfCommpanies = len(result["details"][key]['companies'])
    if  numberOfCommpanies == 0:
        return value['average'], 0, 0, numberOfCommpanies
    return value['average'], result["details"][key]['companies'][0]['days'], result["details"][key]['companies'][-1]['days'], numberOfCommpanies



for (key_date1,value_date1),(key_date2,value_date2) in zip(result1['details'].items(),result2['details'].items()):
    cols = st.columns(2)
    with cols[0]:
        st.markdown("Date 1")
        average1, max_value1, min_value1, numberOfCommpanies1 = showSalesPersonData(result1,key_date1,value_date1)
        if numberOfCommpanies1>0:
            with st.expander("Explore The Companies With Their Waiting Days"):
                filter_by = st.text_input("Search About ... 1 for "+key_date1).lower()
                companies = [ company for company in value_date1['companies']   if company['name'].lower().__contains__(filter_by)]
                st.markdown("### Number of Results: "+str(len(companies)))
                st.divider()
                for company in companies:
                    st.write(company['name'],company['days'])
                    st.markdown(f"> from {company['waiting_details'][stage1].date()} to {company['waiting_details'][stage2].date()}")
                    st.divider()

    with cols[1]:
        st.markdown("Date 2")
        average2, max_value2, min_value2, numberOfCommpanies2 = showSalesPersonData(result2,key_date2,value_date2)
        if numberOfCommpanies2>0:
            with st.expander("Explore The Companies With Their Waiting Days"):
                filter_by = st.text_input("Search About ... 2 for "+key_date2).lower()
                companies = [ company for company in value_date2['companies']   if company['name'].lower().__contains__(filter_by)]
                st.markdown("### Number of Results: "+str(len(companies)))
                st.divider()
                for company in companies:
                    st.write(company['name'],company['days'])
                    st.markdown(f"> from {company['waiting_details'][stage1].date()} to {company['waiting_details'][stage2].date()}")
                    st.divider()

    st.divider()
    st.subheader(key_date1.capitalize())

    st.write("Average Waiting Days ",average1 - average2)

    if numberOfCommpanies1>0 and numberOfCommpanies2>0:
        st.write("Maximum Waiting Days ",max_value1 - max_value2)
    if numberOfCommpanies1>0 and numberOfCommpanies2>0:
        st.write("Minimum Waiting Days ",min_value1 - min_value2)

    st.markdown("> If It's Posative Number this means that is Improvment by 'The Number ")
    st.divider()


st.markdown("# Total waiting Result")
st.divider()
cols = st.columns(2)
with cols[0]:
    st.write("Number of Companies: ",len(result1["result"]['companies'])," With in this range")
    if len(result1["result"]['companies']) >0:
        st.write("Average Days Between the Two Stages: ",result1['result']['average'])
        st.write("Max Waiting Days: ",result1["result"]['companies'][0]['days'])
        st.write("Min Waiting Days: ",result1["result"]['companies'][-1]['days'])

        with st.expander("Explore The Companies With Their Waiting Days"):
            filter_by = st.text_input("Search About ... 1 for Total").lower()
            companies = [ company for company in result1["result"]['companies']   if company['name'].lower().__contains__(filter_by)]
            st.markdown("### Number of Results: "+str(len(companies)))
            st.divider()
            for company in companies:
                st.write(company['name'],company['days'])
                st.markdown(f"> from {company['waiting_details'][stage1].date()} to {company['waiting_details'][stage2].date()}")
                st.divider()
                

with cols[1]:
    st.write("Number of Companies: ",len(result2["result"]['companies'])," With in this range")
    if len(result2["result"]['companies']) >0:
        st.write("Average Days Between the Two Stages: ",result2['result']['average'])
        st.write("Max Waiting Days: ",result2["result"]['companies'][0]['days'])
        st.write("Min Waiting Days: ",result2["result"]['companies'][-1]['days'])
    
        with st.expander("Explore The Companies With Their Waiting Days"):
            filter_by = st.text_input("Search About ... 2 for Total").lower()
            companies = [ company for company in result2["result"]['companies']   if company['name'].lower().__contains__(filter_by)]
            st.markdown("### Number of Results: "+str(len(companies)))
            st.divider()
            for company in companies:
                st.write(company['name'],company['days'])
                st.markdown(f"> from {company['waiting_details'][stage1].date()} to {company['waiting_details'][stage2].date()}")
                st.divider()
    

st.divider()



# stage1.capitalize()+" to "+stage2.capitalize()+ 
# st.subheader("Date Range 2")
# result2 = measure.stageToStage(filtered_data2, stage1,stage2)



# for key,value in result2['details'].items():

#     with cols[1]:

#         st.subheader(key.capitalize())
#         st.write("Number of Companies: ",len(result2["details"][key]['companies'])," With in this range")
#         if len(result2["details"][key]['companies']) >0:
#             st.write("Average days between the 2 Stages: ",value['average'])
#             st.write("Max Waiting Days: ",result2["details"][key]['companies'][0]['days'])
#             st.write("Min Waiting Days: ",result2["details"][key]['companies'][-1]['days'])
#         else:
#             st.subheader("Have No Companies")
        

# st.subheader("Total waiting Result")
# st.write("Number of Companies: ",len(result2["result"]['companies'])," With in this range")
# if len(result2["result"]['companies']) >0:
#     st.write("Average Days Between the Two Stages: ",result2['result']['average'])
#     st.write("Max Waiting Days: ",result2["result"]['companies'][0]['days'])
#     st.write("Min Waiting Days: ",result2["result"]['companies'][-1]['days'])
    
# st.write(len(filtered_data2[index].stagesModel.companies))
# st.write(result2)
st.divider()



# -----------------------------
# Compare ranges side by side in chart
# -----------------------------
# st.subheader("Comparison: Average Duration by Person")

# persons = list(result1['details'].keys())
# values_range1 = [float(result1['details'][p]) for p in persons]
# values_range2 = [float(result2['details'][p]) for p in persons]


# comparison_df = pd.DataFrame({
#     'Salesperson': persons,
#     f'Range 1 ({start_date1} to {end_date1})': values_range1,
#     f'Range 2 ({start_date2} to {end_date2})': values_range2
# })

# # Transform data for Altair
# comparison_melted = comparison_df.melt(id_vars='Salesperson', var_name='Range', value_name='Value')

# chart = alt.Chart(comparison_melted).mark_bar().encode(
#     x=alt.X('Salesperson:N', title='Salesperson'),
#     y=alt.Y('Value:Q', title=f"Average Days from {stage1.capitalize()} to {stage2.capitalize()}"),
#     color='Range:N',
#     tooltip=['Salesperson', 'Range', 'Value']
# ).properties(width=700, height=400)

# st.altair_chart(chart)

# st.header("Comparison of Final Stages Between Two Date Ranges"),


# Example: get last stages for each range
lastStages1, names1, _ = SalesPerson.getTotalCompanyLifeStages(filtered_data1)
lastStages2, names2, _ = SalesPerson.getTotalCompanyLifeStages(filtered_data2)
countMeasure = CountMeasure()
result1, companies1 = countMeasure.countPerStage(filtered_data1)
result2, companies2 = countMeasure.countPerStage(filtered_data2)
# st.write(result) 

for (name,salesData1),(_,salesData2) in zip(result1['details'].items(),result2['details'].items()):
    total =0
    for key,val in salesData1.items():
        total+=val
    with st.expander(f"{name.capitalize()} Per Stage"):
        df1 = pd.DataFrame(list(salesData1.items()), columns=['Stage', 'Count'])
        df2 = pd.DataFrame(list(salesData2.items()), columns=['Stage', 'Count'])
        comparison_df = pd.merge(df1, df2, on='Stage', how='outer').fillna(0)

        st.write(comparison_df)

# Count how many salespeople ended up in each stage
stage_counts1 = pd.Series(lastStages1).value_counts().reset_index()
stage_counts1.columns = ['Stage', f'Count Range 1 ({start_date1} to {end_date1})']

stage_counts2 = pd.Series(lastStages2).value_counts().reset_index()
stage_counts2.columns = ['Stage', f'Count Range 2 ({start_date2} to {end_date2})']

# Merge the two counts by stage
comparison_df = pd.merge(stage_counts1, stage_counts2, on='Stage', how='outer').fillna(0)
st.write(comparison_df)
# Melt for Altair (Range 1 vs Range 2)
comparison_melted = comparison_df.melt(
    id_vars='Stage',
    var_name='Range',
    value_name='Count'
)

# Optional: set a logical stage order
stage_order = ["Leads", "Orphans", "We called", "Meeting", "Gathering",
            "NDA", "POC", "Qualified", "Not qualified", "Client POC",
            "Proposition", "Won", "Lost"]

# Create grouped bar chart (stage on x, count on y)
chart = alt.Chart(comparison_melted).mark_bar().encode(
    x=alt.X('Stage:N', sort=stage_order, title='Stage'),
    y=alt.Y('Count:Q', title='Number of Salespeople'),
    color=alt.Color('Range:N', title='Date Range'),
    tooltip=['Stage', 'Range', 'Count']
).properties(
    width=800,
    height=500
)

st.altair_chart(chart, use_container_width=True)
# except Exception as e:
#     st.subheader("Please Choose Two Stages ...")