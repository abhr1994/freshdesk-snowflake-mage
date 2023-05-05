import streamlit as st
from snowflake.snowpark import Session
import plotly.express as px

st.title('❄️ Streamlit  - Snowflake ❄️ ')


# Establish Snowflake session
@st.cache_resource
def create_session():
    return Session.builder.configs(st.secrets.snowflake).create()


session = create_session()
st.success("Connected to Snowflake!")


# Load data table
@st.cache_data
def load_data(table_name):
    st.write(f"Here's some sample data from `{table_name}`:")
    table = session.table(table_name)
    table = table.limit(10)
    table = table.collect()
    return table


# Select and display data table
table_name = "resolution_time_graph"

# Display data table
with st.expander("See Table Data"):
    df = load_data(table_name)
    st.dataframe(df)

# Plot few graphs
fig1 = px.bar(df, x='ticket_resolution_in_hours', y='total_tickets', color='total_tickets')
st.plotly_chart(fig1, use_container_width=True)

df_tickets = session.table(".tickets_per_company").collect()
fig2 = px.bar(df_tickets, x='company_name', y='ticket_count', color='ticket_count')
st.plotly_chart(fig2, use_container_width=True)
