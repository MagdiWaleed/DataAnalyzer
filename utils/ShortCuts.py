import streamlit as st
import datetime
from datetime import timedelta

class DateShortCut():
    def __init__(self):
        self.renderUI()
    def renderUI(self):
        timeNome = datetime.datetime.now()
        cols = st.columns(4)
        for i,col in enumerate(cols):
            current_month = timeNome.month - i 
            with col:
                st.button(current_month)

                

            

        