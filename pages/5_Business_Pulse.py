import streamlit as st
import pandas as pd
import altair as alt
import datetime
from models.SalesPerson import SalesPerson
from models.TotalModel import TotalSalesPerson

st.set_page_config(page_title="Business Pulse", page_icon="📈", layout="wide")

st.title("📈 Business Pulse: Performance Trends")
st.markdown("Track the velocity of your business activities over time.")

# 1. Enforce Data
if "data" not in st.session_state or "meeting_data" not in st.session_state:
    st.warning("Data is missing. Please upload files in the 'Upload Files' page.")
    st.stop()

# data = 'data' for Pipeline 1 (Stage details) -> Used for Leads trend
# meeting_data = 'meeting_data' for Pipeline 2 (Totals) -> Used for Meetings/Calls
data_stage = st.session_state['data']
data_meet = st.session_state['meeting_data']

# 2. Controls
col_filters = st.columns(3)
with col_filters[0]:
    freq = st.selectbox("Frequency", ["W", "M", "D"], index=0, format_func=lambda x: "Weekly" if x=="W" else ("Monthly" if x=="M" else "Daily"))

# 3. Data Processing for Time Series (Pandas Magic)

# --- A. Leads Trend ---
# Companies have 'leads' date. 
all_companies = SalesPerson.getTotalCompanies(data_stage)
leads_data = []
for c in all_companies:
    if c.leads and not pd.isna(c.leads):
        leads_data.append({'Date': c.leads, 'Type': 'New Leads'})

# --- B. Meetings Trend ---
# meeting_data is list of TotalSalesPerson
# Each TotalSalesPerson has totalModel -> meetingModels (list of MeetingModel) 
# MeetingModel has .date
meetings_data = []
for tsp in data_meet:
    # tsp is TotalSalesPerson
    if tsp.totalModel and tsp.totalModel.meetingsModel:
        for m in tsp.totalModel.meetingsModel:
            if m.date and not pd.isna(m.date) and not isinstance(m.date, str): 
                # Note: code in PreProcessingTotalsPipeLine suggests default date replacement for placeholders?
                # We should filter valid dates.
                if m.date.year > 2000: # Simple sanity check
                    meetings_data.append({'Date': m.date, 'Type': 'Meetings Held'})

# --- C. Calls Trend ---
# TotalSalesPerson -> totalModel -> callsModel (list of CallsModel) -> .date, .amount
calls_data = []
for tsp in data_meet:
    if tsp.totalModel and tsp.totalModel.callsModel:
        for c in tsp.totalModel.callsModel:
            if c.date and not pd.isna(c.date) and not isinstance(c.date, str):
                if c.date.year > 2000:
                    # Note: one CallsModel entry might represent multiple calls (amount)
                    # We should probably sum the amount for that day, or just count entry?
                    # Looking at TotalModel definitions, CallsModel has 'amount'.
                    # Let's add N entries or just sum later. Easier to just store amount.
                    calls_data.append({'Date': c.date, 'Type': 'Calls Made', 'Count': c.amount})

# Create DataFrames
df_leads = pd.DataFrame(leads_data)
if not df_leads.empty:
    df_leads['Count'] = 1 # Each entry is 1 lead

df_meetings = pd.DataFrame(meetings_data)
if not df_meetings.empty:
    df_meetings['Count'] = 1

df_calls = pd.DataFrame(calls_data) # Already has 'Count' or need to handle if empty

# Combine
frames = []
if not df_leads.empty: frames.append(df_leads)
if not df_meetings.empty: frames.append(df_meetings)
if not df_calls.empty: frames.append(df_calls)

if not frames:
    st.warning("No valid date data found for trends.")
    st.stop()

df_all = pd.concat(frames)
df_all['Date'] = pd.to_datetime(df_all['Date'])

# Resample by Frequency
# Group by Date(Freq) and Type
df_grouped = df_all.groupby([pd.Grouper(key='Date', freq=freq), 'Type'])['Count'].sum().reset_index()

# 4. Visualization

# --- Metric Cards (Last 30 Days) ---
st.divider()
now = datetime.datetime.now()
last_30 = now - datetime.timedelta(days=30)
df_recent = df_all[df_all['Date'] >= last_30]

m1, m2, m3 = st.columns(3)
with m1:
    count = df_recent[df_recent['Type']=='New Leads']['Count'].sum()
    st.metric("New Leads (Last 30 Days)", int(count))
with m2:
    count = df_recent[df_recent['Type']=='Meetings Held']['Count'].sum()
    st.metric("Meetings (Last 30 Days)", int(count))
with m3:
    count = df_recent[df_recent['Type']=='Calls Made']['Count'].sum()
    st.metric("Calls (Last 30 Days)", int(count))

st.divider()

# --- Main Chart ---
# Multi-line chart
chart = alt.Chart(df_grouped).mark_line(point=True).encode(
    x=alt.X('Date:T', title='Date'),
    y=alt.Y('Count:Q', title='Volume'),
    color=alt.Color('Type:N', scale=alt.Scale(scheme='category10')),
    tooltip=['Date', 'Type', 'Count']
).properties(
    height=450,
    title="Activity Trends"
).interactive()

st.altair_chart(chart, use_container_width=True)

# --- Data Table (Optional) ---
with st.expander("View Raw Aggregated Data"):
    st.dataframe(df_grouped.sort_values('Date', ascending=False), use_container_width=True)

st.success("""
### 💡 Business Insights: What this page tells you
This **Business Pulse** dashboard is your "speedometer". It tracks the velocity of your team's key activities over time:
- **New Leads**: Are we filling the top of the funnel consistently?
- **Meetings Held**: Are we effectively engaging with prospects?
- **Calls Made**: Is our outreach effort sustained?

**How to use it:**
- Look for **trends**: Is the line going up or down? A drop in leads today means fewer sales next month.
- Check the **Last 30 Days** metrics to see immediate performance.
- Use this to spot **seasonality** or the impact of specific campaigns.
""")
