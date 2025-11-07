import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="MSH Startup Innovation Dashboard", layout="wide")
st.title(" MSH Startup Innovation Dashboard")
st.markdown("Gain insights into startup performance, funding, and innovation trends across India.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("startup_data.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()), index=len(df["Year"].unique()) - 1)
region = st.sidebar.selectbox("Select Region", ["All"] + sorted(df["Region"].unique()))
program = st.sidebar.selectbox("Select Program", ["All"] + sorted(df["Program"].unique()))

filtered_df = df[df["Year"] == year]
if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]
if program != "All":
    filtered_df = filtered_df[filtered_df["Program"] == program]

# KPIs 
st.subheader(f" Year: {year}")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Startups", len(filtered_df))
col2.metric("Avg Funding (M$)", f"{filtered_df['Funding(Million$)'].mean():.2f}")
col3.metric("Avg Revenue (M$)", f"{filtered_df['Revenue(Million$)'].mean():.2f}")
col4.metric("Innovation Index", f"{filtered_df['Innovation_Score'].mean():.1f}")

#  Visualizations
col5, col6 = st.columns(2)

with col5:
    fig1 = px.bar(filtered_df, x="Startup", y="Funding(Million$)", color="Region",
                  title="Funding by Startup", text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    fig2 = px.scatter(filtered_df, x="Funding(Million$)", y="Revenue(Million$)", color="Startup",
                      size="Employees", hover_name="Startup",
                      title="Funding vs Revenue (Startup Performance)")
    st.plotly_chart(fig2, use_container_width=True)

#Innovation Trend 
trend_df = df.groupby("Year")[["Funding(Million$)", "Innovation_Score"]].mean().reset_index()
fig3 = px.line(trend_df, x="Year", y=["Funding(Million$)", "Innovation_Score"],
               markers=True, title="Innovation & Funding Trend Over Years")
st.plotly_chart(fig3, use_container_width=True)

# Data Table 
st.markdown("Detailed Data")
st.dataframe(filtered_df)

st.markdown("Insights")
st.info("Startups in 2025 show record innovation and funding growth — especially in programs under *MSH Ignite* and *MSH Accelerator* initiatives.")

