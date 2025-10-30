import streamlit as st
import datetime
import numpy as np
import pandas as pd
import altair as alt
from PipeLines.PreProcessingPipeLine import PreProcessingTotalsPipeLine
from PipeLines.LoadingPipeLine import LoadingPipeLine
from models.TotalModel import TotalSalesPerson
from datetime import timedelta
from PipeLines import PipeLine
from utils.Searchers import Sheet2Searcher


if "meeting_data" not in st.session_state:
    loadingPipeLine = LoadingPipeLine()
    preprocessing = PreProcessingTotalsPipeLine()
    data,names = loadingPipeLine.run()
    data = preprocessing.run(data,names)
    st.session_state['meeting_data'] = data
    
    pipeLine = PipeLine()
    _,  sheet2 = pipeLine.run(return_sheet2=True)
    st.session_state['searcher'] = Sheet2Searcher(sheet2)

data = st.session_state['meeting_data']

switch = st.checkbox("Enable Filtering")
enableComparison = st.checkbox("Enable Comparison")
col2, col3 = st.columns(2)
if switch:
    with col2:
        st.markdown("#### Date Range 1")
        start_date1 = st.date_input("Start Date 1", datetime.datetime.now().date() - timedelta(days=7+4))
        end_date1 = st.date_input("End Date 1", datetime.datetime.now().date()- timedelta(days=7))
    if enableComparison:
        with col3:
            st.markdown("#### Date Range 2")
            start_date2 = st.date_input("Start Date 2", datetime.datetime.now().date() - timedelta(days=4))
            end_date2 = st.date_input("End Date 2", datetime.datetime.now().date())
        st.divider()

    data1 = TotalSalesPerson.filter_by(
                                    data,
                                   datetime.datetime.combine(start_date1, datetime.time.min),
                                    datetime.datetime.combine(end_date1, datetime.time.max)
                                    )
    if enableComparison:
        data2 = TotalSalesPerson.filter_by(
                                        data,
                                    datetime.datetime.combine(start_date2, datetime.time.min),
                                        datetime.datetime.combine(end_date2, datetime.time.max)
                                        )

if enableComparison and switch:
    result1 = TotalSalesPerson.getTotalMeetings(data1)
    result2 = TotalSalesPerson.getTotalMeetings(data2)
    
    result_calls1 = TotalSalesPerson.getTotalSuccessfullCalls(data1)
    result_calls2 = TotalSalesPerson.getTotalSuccessfullCalls(data2)

    result_total_calls1 = TotalSalesPerson.getTotalCalls(data1)
    result_total_calls2 = TotalSalesPerson.getTotalCalls(data2)

    st.markdown("## Per SalesPerson")
    for ((salesPerson1, value1),(salesPerson2, value2)),((salesPerson_calls1, value_calls1),(salesPerson_calls2, value_calls2)),((salesPerson_total_calls1, value_total_calls1),(salesPerson_total_calls2, value_total_calls2)) in zip(zip(result1['details'].items(),result2['details'].items()),zip(result_calls1['details'].items(),result_calls2['details'].items()),zip(result_total_calls1['details'].items(),result_total_calls2['details'].items())):
        st.markdown(f"### {salesPerson1.capitalize()}")
        col1,col2 = st.columns(2)
        
        with col1:
            st.markdown(f"##### Date 1")
            st.write("Number of Meetings: ",len(value1))
            st.write("Number of Successful Calls: ",len(value_calls1))
            st.write("Number of Total Calls: ",np.sum([t['amount'] for t in value_total_calls1]))
            


            if len(value1) > 0:
                with st.expander("Explore Meetings Companies"):
                    placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in value1])
                    for key,value in placeholder.items():
                        st.write(f"{key}: ",value)
                    st.divider()
                    for t in value1:
                        st.write(" ",t['name'],": ",t['date'], " --> ",st.session_state['searcher'].getModel(t['name']))
            else:
                st.markdown(">Have No Meetings")
            
            if len(value_calls1) > 0:
                with st.expander("Explore Successful Calls"):
                    placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in value_calls1])
                    for key,value in placeholder.items():
                        st.write(f"{key}: ",value)
                    st.divider()
                    for t in value_calls1:
                        st.write(" ",t['name'],": ",t['date'], " --> ",st.session_state['searcher'].getModel(t['name']))
            else:
                st.markdown(">Have No Successful Calls")
          
            if len(value_total_calls1) > 0:
                with st.expander("Explore Total Calls"):
                    for t in value_total_calls1:
                        st.write(" ",t['date'],": ",t['amount'])
            else:
                st.markdown(">Have No Total Calls")
            
        with col2:
            st.markdown(f"##### Date 2")
            st.write("Number of Meetings: ",len(value2))
            st.write("Number of Successful Calls: ",len(value_calls2))
            st.write("Number of Total Calls: ",np.sum([t['amount'] for t in value_total_calls2]))
            if len(value2) > 0:
                with st.expander("Explore Meetings Companies"):
                    placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in value2])
                    for key,value in placeholder.items():
                        st.write(f"{key}: ",value)
                    st.divider()
                    for t in value2:
                        st.write(" ",t['name'],": ",t['date']," --> ",st.session_state['searcher'].getModel(t['name']))
            else:
                st.markdown(">Have No Meetings")
            if len(value_calls2) > 0:
                with st.expander("Explore Calls Companies"):
                    placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in value_calls2])
                    for key,value in placeholder.items():
                        st.write(f"{key}: ",value)
                    st.divider()
                    for t in value_calls2:
                        st.write(" ",t['name'],": ",t['date']," --> ",st.session_state['searcher'].getModel(t['name']))
            else:
                st.markdown(">Have No Calls")

            if len(value_total_calls2) > 0:
                with st.expander("Explore Total Calls"):
                    for t in value_total_calls2:
                        st.write(" ",t['date'],": ",t['amount'])
            else:
                st.markdown(">Have No Total Calls")
            
        st.divider()
    st.markdown("## In Total")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown(f"##### Date 1")
        st.write("Number of Meetings: ",len(result1['total']))
        st.write("Number of Successful Calls: ",len(result_calls1['total']))
        st.write("Number of Total Calls: ",np.sum([ t['amount'] for t in result_total_calls1['total']]))

        if len(result1['total']) > 0:
            with st.expander("Explore Meetings"):
                placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in result1['total']])
                for key,value in placeholder.items():
                    st.write(f"{key}: ",value)
                st.divider()

                for t in result1['total']:
                    st.write(" ",t['name'],": ",t['date'], " --> ",st.session_state['searcher'].getModel(t['name']))
        else:
            st.markdown(">Have No Meetings")

        if len(result_calls1['total']) > 0:
            with st.expander("Explore Successfull Calls"):
                placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in result_calls1['total']])
                for key,value in placeholder.items():
                    st.write(f"{key}: ",value)
                st.divider()
                for t in result_calls1['total']:
                    st.write(" ",t['name'],": ",t['date'], " --> ", st.session_state['searcher'].getModel(t['name']))
        else:
            st.markdown(">Have No Calls")

        if len(result_total_calls1['total']) > 0:
            with st.expander("Explore Total Calls"):
                for t in result_total_calls1['total']:
                    st.write(" ",t['date'],": ",t['amount'])
        else:
            st.markdown(">Have No Total Calls")
            

    with col2:
        st.markdown(f"##### Date 2")
        st.write("Number of Meetings: ",len(result2['total']))
        st.write("Number of Successful Calls: ",len(result_calls2['total']))
        st.write("Number of Total Calls: ",np.sum([ t['amount'] for t in result_total_calls2['total']]))

        if len(result2['total']) > 0:
            with st.expander("Explore Meetings "):
                placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in result2['total']])
                for key,value in placeholder.items():
                    st.write(f"{key}: ",value)
                st.divider()
                for t in result2['total']:
                    st.write(" ",t['name'],": ",t['date'], " --> ", st.session_state['searcher'].getModel(t['name']))
        else:
            st.markdown(">Have No Meetings")
        if len(result_calls2['total']) > 0:
            with st.expander("Explore Successfull Calls"):
                placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in result_calls2['total']])
                for key,value in placeholder.items():
                    st.write(f"{key}: ",value)
                st.divider()
                for t in result_calls2['total']:
                    st.write(" ",t['name'],": ",t['date']," --> ", st.session_state['searcher'].getModel(t['name']))
        else:
            st.markdown(">Have No Calls")

        if len(result_total_calls2['total']) > 0:
            with st.expander("Explore Total Calls"):
                for t in result_total_calls2['total']:
                    st.write(" ",t['date'],": ",t['amount'])
        else:
            st.markdown(">Have No Total Calls")
    st.divider()

    per_salesperson_data = []
    for salesperson, value1 in result1['details'].items():
        value2 = result2['details'].get(salesperson, [])
        per_salesperson_data.append({
            'Salesperson': salesperson.capitalize(),
            'Date Range': f"{start_date1} → {end_date1}",
            'Meetings': len(value1)
        })
        per_salesperson_data.append({
            'Salesperson': salesperson.capitalize(),
            'Date Range': f"{start_date2} → {end_date2}",
            'Meetings': len(value2)
        })

    # Add a total row for overall comparison
    per_salesperson_data.append({
        'Salesperson': 'Total',
        'Date Range': f"{start_date1} → {end_date1}",
        'Meetings': len(result1['total'])
    })
    per_salesperson_data.append({
        'Salesperson': 'Total',
        'Date Range': f"{start_date2} → {end_date2}",
        'Meetings': len(result2['total'])
    })

    df_compare = pd.DataFrame(per_salesperson_data)

    st.markdown("### Meetings Comparison per Sales person")

    # --- Proper side-by-side grouped bar chart ---
    chart = (
        alt.Chart(df_compare)
        .mark_bar(size=40, cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X('Salesperson:N', title='Salesperson', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Meetings:Q', title='Number of Meetings'),
            color=alt.Color('Date Range:N', title='Date Range'),
            xOffset='Date Range:N',  # This is the key! Groups the bars side-by-side
            tooltip=['Salesperson', 'Date Range', 'Meetings']
        )
        .properties(height=400)
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_legend(titleFontSize=13, labelFontSize=12)
    )

    st.altair_chart(chart, use_container_width=True)

    



else:
    if switch:
        result = TotalSalesPerson.getTotalMeetings(data1)
        
        result_calls = TotalSalesPerson.getTotalSuccessfullCalls(data1)
        
        result_total_calls = TotalSalesPerson.getTotalCalls(data1)
    
    else:        
        result = TotalSalesPerson.getTotalMeetings(data)
    
        result_calls = TotalSalesPerson.getTotalSuccessfullCalls(data)
        
        result_total_calls = TotalSalesPerson.getTotalCalls(data)
    
    for (salesPerson, value),(salesPerson_calls, value_calls),(salesPerson_total_calls, value_total_calls) in zip(result['details'].items(),result_calls['details'].items(),result_total_calls['details'].items(),):
        st.markdown(f"##### {salesPerson.capitalize()}")
        st.write("Number of Meetings: ",len(value))
        st.write("Number of Successful Calls: ",len(value_calls))
        st.write("Number of Total Calls: ",np.sum([t['amount'] for t in value_total_calls]))

        if len(value) > 0:
            with st.expander("Explore Meetings "):
                placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in value])
                for key,value_dash in placeholder.items():
                    st.write(f"{key}: ",value_dash)
                st.divider()
                for t in value:
                    st.write(" ",t['name'],": ",t['date']," --> ", st.session_state['searcher'].getModel(t['name']))

        if len(value_calls) > 0:
                with st.expander("Explore Calls Companies"):
                    placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in value_calls])
                    for key,value_dash in placeholder.items():
                        st.write(f"{key}: ",value_dash)
                    st.divider()
                    for t in value_calls:
                        st.write(" ",t['name'],": ",t['date']," --> ", st.session_state['searcher'].getModel(t['name']))
        else:
            st.markdown(">Have No Calls")

        if len(value_total_calls) > 0:
            with st.expander("Explore Total Calls"):
                for t in value_total_calls:
                    st.write(" ",t['date'],": ",t['amount'])
        else:
            st.markdown(">Have No Total Calls")

    st.markdown("#### Meetings In Total")
    st.write("Number of Meetings: ",len(result['total']))
    st.write("Number of Successful Calls: ",len(result_calls['total']))
    st.write("Number of Total Calls: ",np.sum([ t['amount'] for t in result_total_calls['total']]))

    if len(result['total']) > 0:
        with st.expander("Explore Meeting "):
            placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in result['total']])
            for key,value_dash in placeholder.items():
                st.write(f"{key}: ",value_dash)
            st.divider()
            for t in result['total']:
                st.write(" ",t['name'],": ",t['date']," --> ", st.session_state['searcher'].getModel(t['name']))
    else:
        st.markdown(">Have No Meetings")
    if len(result_calls['total']) > 0:
        with st.expander("Explore Successfull Calls "):
            placeholder = st.session_state['searcher'].countFrequency([t['name'] for t in result_calls['total']])
            for key,value_dash in placeholder.items():
                st.write(f"{key}: ",value_dash)
            st.divider()
            for t in result_calls['total']:
                st.write(" ",t['name'],": ",t['date']," --> ", st.session_state['searcher'].getModel(t['name']))
    else:
        st.markdown(">Have No Calls")

    if len(result_total_calls['total']) > 0:
        with st.expander("Explore Total Calls"):
            for t in result_total_calls['total']:
                st.write(" ",t['date'],": ",t['amount'])
    else:
        st.markdown(">Have No Total Calls")
  
