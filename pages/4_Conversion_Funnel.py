import streamlit as st
import pandas as pd
import altair as alt
from models.SalesPerson import SalesPerson

st.set_page_config(page_title="Conversion Funnel", page_icon="🔻", layout="wide")

st.title("🔻 Conversion Funnel Analysis")
st.markdown("Analyze the drop-off rates between sales stages.")

# 1. Enforce Data
if "data" not in st.session_state:
    st.warning("Upload data is required. Please go to the 'Upload Files' page.")
    st.stop()

data = st.session_state['data']

# 2. Define Stage Map (Full List)
full_stage_map = {
    'Leads': 'leads',
    'We Called': 'we_called',
    'Meeting': 'meeting',
    'NDA': 'nda',
    'Gathering': 'gathering',
    'POC': 'poc',
    'Client POC': 'client_poc',
    'Qualified': 'qualified',  # Split Path A
    'Not Qualified': 'not_qualified', # Split Path B
    'Proposition': 'proposition',
    'Won': 'won', # End State A
    'Lost': 'lost', # End State B
    'Orphans': 'orphans' # Excluded by default
}

# 3. Interactive Reordering
st.subheader("⚙️ Funnel Configuration")
default_order = [
    'Leads', 'We Called', 'Meeting', 'NDA', 'Gathering', 
    'POC', 'Client POC', 'Qualified', 'Not Qualified', 
    'Proposition', 'Won', 'Lost'
]

selected_stages = st.multiselect(
    "Select and Reorder Stages for Funnel:",
    options=list(full_stage_map.keys()),
    default=default_order
)

if not selected_stages:
    st.warning("Please select at least one stage.")
    st.stop()

# 4. Calculation Logic
# Flatten all companies
all_companies = SalesPerson.getTotalCompanies(data)

funnel_data = []
total_leads = 0
prev_count = 0

# Use the USER defined order
for display_name in selected_stages:
    attr_name = full_stage_map[display_name]
    
    # Count how many companies have a value (date) for this attribute
    # Improved Count: explicitly check for valid dates if needed, but 'is not None' is mostly safe if model is clean
    count = sum(1 for c in all_companies if getattr(c, attr_name, None) is not None)
    
    # Special Handling for Leads (Base of Funnel)
    if display_name == selected_stages[0]:
        total_leads = count
        conversion_from_leads = 100.0
        conversion_from_prev = 100.0
    else:
        conversion_from_leads = (count / total_leads * 100) if total_leads > 0 else 0
        conversion_from_prev = (count / prev_count * 100) if prev_count > 0 else 0
    
    funnel_data.append({
        'Stage': display_name,
        'Count': count,
        'From First Stage (%)': round(conversion_from_leads, 1),
        'From Prev Stage (%)': round(conversion_from_prev, 1),
        'Drop-off (%)': round(100 - conversion_from_prev, 1) if display_name != selected_stages[0] else 0
    })
    prev_count = count # Update previous for next iteration

df_funnel = pd.DataFrame(funnel_data)

# 5. Visuals
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Funnel Metrics")
    st.dataframe(
        df_funnel[['Stage', 'Count', 'From First Stage (%)', 'From Prev Stage (%)']],
        column_config={
            "From First Stage (%)": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=100),
            "From Prev Stage (%)": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=100),
        },
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("Visual Funnel Flow")
    
    base = alt.Chart(df_funnel).encode(
        y=alt.Y('Stage:N', sort=selected_stages, title=None),
        tooltip=['Stage', 'Count', 'From First Stage (%)', 'From Prev Stage (%)']
    )
    
    # Horizontal Bar Chart to represent Funnel
    bars = base.mark_bar().encode(
        x=alt.X('Count:Q', title='Number of Companies'),
        color=alt.Color('From First Stage (%)', scale=alt.Scale(scheme='tealblues'), legend=None)
    )
    
    text = base.mark_text(align='left', dx=2).encode(
        x='Count:Q',
        text=alt.Text('Count:Q', format=',')
    )
    
    chart = (bars + text).properties(height=max(400, len(selected_stages) * 40))
    st.altair_chart(chart, use_container_width=True)

st.divider()

st.success("""
### 💡 Business Insights: Funnel & Path Analysis
This page allows you to analyze **Sequential** and **Conditional** paths.

**Understanding the Flow:**
1.  **Sequential Stages**: Steps like *Leads -> We Called -> Meeting* usually happen in order. A drop-off here is a simple efficiency loss.
2.  **Conditional Paths (Split Logic)**:
    -   **Qualified / Not Qualified**: These are branches. You can check the "Not Qualified" count to see how many leads you are filtering out early (which saves time!).
    -   **Won / Lost**: These are final outcomes.
    -   *Tip: Move 'Not Qualified' or 'Lost' to the bottom of the list above to see them separately, or keep them next to their decision point.*

**Key Metrics:**
- **From First Stage (%)**: Shows the overall survival rate from the top of your current list.
- **From Prev Stage (%)**: Shows the immediate conversion. **Watch out** if you put 'Lost' right after 'Won', this % might look weird because they are mutually exclusive paths, not sequential steps!
""")

