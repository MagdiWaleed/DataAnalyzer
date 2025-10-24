import streamlit as st
import datetime
import numpy as np
from PipeLines import PipeLine
from filters.DatesFilter import DatesFilter
from measures.Between import BetweenMeasure
from models.SalesPerson import SalesPerson
import pandas as pd
import altair as alt

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Stage Comparison Dashboard",
    layout="wide"
)

st.title("📊 Stage-to-Stage Comparison")

# -----------------------------
# Run pipeline and get data
# -----------------------------
pipeLine = PipeLine()
data = pipeLine.run()

# -----------------------------
# Sidebar: select columns and date ranges
# -----------------------------
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
    start_date1 = st.date_input("Start Date 1", datetime.date(2025, 9, 1))
    end_date1 = st.date_input("End Date 1", datetime.date(2025, 9, 30))

with col3:
    st.markdown("### Date Range 2")
    start_date2 = st.date_input("Start Date 2", datetime.date(2025, 10, 1))
    end_date2 = st.date_input("End Date 2", datetime.date(2025, 10, 20))

st.divider()
try:
    stage1 = stage1[0]
    stage2 = stage2[0]
    st.markdown(f"> 0 Means The Company Goes from {stage1.capitalize()} to {stage2.capitalize()} at the same Day")
    # -----------------------------
    # Filter data by first date range
    # -----------------------------

    filter1 = DatesFilter()
    filtered_data1 = filter1([stage1,stage2],data, datetime.datetime.combine(start_date1, datetime.time.min),
                                        datetime.datetime.combine(end_date1, datetime.time.max))

    # -----------------------------
    # Filter data by second date range
    # -----------------------------
    filter2 = DatesFilter()
    filtered_data2 = filter2([stage1,stage2],data, datetime.datetime.combine(start_date2, datetime.time.min),
                                        datetime.datetime.combine(end_date2, datetime.time.max))

    # -----------------------------
    # Apply BetweenMeasure
    # -----------------------------
    measure = BetweenMeasure()

    st.subheader("Date Range 1")
    result1 = measure.stageToStage(filtered_data1, stage1,stage2)
    index = 1
    # st.write(len(filtered_data1[index].stagesModel.companies))
    # st.write(result1)

    NUM_COLUMNS = 3
    cols = st.columns(NUM_COLUMNS)

    for i,(key,value) in enumerate(result1['details'].items()):
        col_index = i % NUM_COLUMNS

        with cols[col_index]:

            st.subheader(key.capitalize())
            st.write("Number of Companies: ",len(filtered_data1[i].stagesModel.companies)," With in this range")
            st.write("Average days between the 2 Stages: ",value)
            pass
    totalCompanies = SalesPerson.getTotalCompanies(filtered_data1)
    st.subheader("Total waiting Result")
    st.write("Number of Companies: ",len(totalCompanies)," With in this range")
    st.write("Average Days Between the Two Stages: ",result1['result'])
        
        

    st.divider()



    # stage1.capitalize()+" to "+stage2.capitalize()+ 
    st.subheader("Date Range 2")
    result2 = measure.stageToStage(filtered_data2, stage1,stage2)


    cols = st.columns(NUM_COLUMNS)

    for i,(key,value) in enumerate(result2['details'].items()):
        col_index = i % NUM_COLUMNS

        with cols[col_index]:

            st.subheader(key.capitalize())
            st.write("Number of Companies: ",len(filtered_data2[i].stagesModel.companies)," With in this range")
            st.write("Average days between the 2 Stages: ",value)
            pass

    totalCompanies = SalesPerson.getTotalCompanies(filtered_data2)
    st.subheader("Total waiting Result")
    st.write("Number of Companies: ",len(totalCompanies)," With in this range")
    st.write("Average Days Between the Two Stages: ",result2['result'])
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

    # Count how many salespeople ended up in each stage
    stage_counts1 = pd.Series(lastStages1).value_counts().reset_index()
    stage_counts1.columns = ['Stage', f'Count Range 1 ({start_date1} to {end_date1})']

    stage_counts2 = pd.Series(lastStages2).value_counts().reset_index()
    stage_counts2.columns = ['Stage', f'Count Range 2 ({start_date2} to {end_date2})']

    # Merge the two counts by stage
    comparison_df = pd.merge(stage_counts1, stage_counts2, on='Stage', how='outer').fillna(0)

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
except Exception as e:
    st.subheader("Please Choose Two Stages ...")