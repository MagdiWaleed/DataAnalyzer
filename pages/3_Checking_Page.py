import streamlit as st
from PipeLines import PipeLine
from measures.Count import CountMeasure

countMeasure = CountMeasure()



st.set_page_config(
    page_title="Stage Comparison Dashboard",
    layout="wide"
    
)

st.title("Checking Page")


if "data" not in st.session_state:
    st.warning("Upload data is required. Please go to the 'Upload Files' page.")
    st.stop()

data = st.session_state['data'] 

result,companies = countMeasure.countPerStage(data,unique=True)

with st.expander("Search By Company or Stage"):
    filter_by = st.text_input("Search About ... ").lower()

    st.divider()
    for company in companies['result']:
            if company['name'].lower().__contains__(filter_by) or company['stage'].lower().__contains__(filter_by):
                st.write(company['name'], " --> ",company['stage'])

