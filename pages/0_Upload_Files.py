import streamlit as st
from PipeLines import PipeLine
from utils.Searchers import Sheet2Searcher
import pandas as pd

st.set_page_config(page_title="Upload Files", page_icon="📂")

st.title("📂 Upload Data Files")
st.markdown("Please upload your weekly report Excel files below. You can rename them before processing.")

uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])

if uploaded_files:
    st.divider()
    st.subheader("Rename Files (Optional)")
    
    file_names = []
    
    # Use a form to group inputs and submit button
    with st.form("processing_form"):
        for i, file in enumerate(uploaded_files):
            # Default name without extension
            default_name = file.name.split('.')[0]
            # Unique key for each input
            name = st.text_input(f"Name for {file.name}", value=default_name, key=f"file_name_{i}")
            file_names.append(name)
        
        submitted = st.form_submit_button("Process & Load Data")
        
        if submitted:
            with st.spinner("Processing files..."):
                try:
                    # 1. Initialize Loading Pipeline
                    from PipeLines.LoadingPipeLine import LoadingPipeLine
                    from PipeLines.PreProcessingPipeLine import PreProcessingPipeLine, PreProcessingTotalsPipeLine
                    
                    loading = LoadingPipeLine(uploaded_files=uploaded_files, names=file_names)
                    
                    # 2. Process Main Data (Re-read 1)
                    dfs_main, names_main = loading.run()
                    pre_main = PreProcessingPipeLine()
                    data_main, sheet2 = pre_main.run(dfs_main, names_main)
                    
                    # 3. Process Meeting Data (Re-read 2 - Essential because pipelines modify data in-place)
                    dfs_meet, names_meet = loading.run()
                    pre_total = PreProcessingTotalsPipeLine()
                    data_meet = pre_total.run(dfs_meet, names_meet)
                    
                    # 4. Store in session state
                    st.session_state['data'] = data_main
                    st.session_state['searcher'] = Sheet2Searcher(sheet2)
                    st.session_state['meeting_data'] = data_meet
                    
                    st.success("✅ Data loaded successfully! You can now navigate to the Dashboard.")
                except Exception as e:
                    st.error(f"Error processing files: {str(e)}")
                    st.exception(e)

st.divider()
if "data" in st.session_state:
    st.info(f"Currently loaded: {len(st.session_state['data'])} files.")
else:
    st.warning("No data loaded. Please upload files to proceed.")
