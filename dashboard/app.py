import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from ml.forecast import forecast_cpu

st.set_page_config(layout="wide")

st.title("Predictive Infrastructure Monitoring")

df = pd.read_csv("storage/sample_metrics.csv")

cpu = df["cpu"].iloc[-1]
ram = df["ram"].iloc[-1]
disk = df["disk"].iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric("CPU", f"{cpu}%")
col2.metric("RAM", f"{ram}%")
col3.metric("Disk", f"{disk}%")

prediction = forecast_cpu(df)

st.subheader("CPU Forecast")

if prediction:
    st.metric(
        "Predicted CPU",
        f"{prediction:.2f}%"
    )

st.subheader("CPU Trend + Forecast")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=list(range(len(df))),
        y=df["cpu"],
        mode="lines+markers",
        name="Actual CPU"
    )
)

fig.add_trace(
    go.Scatter(
        x=[len(df)],
        y=[prediction],
        mode="markers",
        name="Forecast",
        marker=dict(size=15)
    )
)

fig.update_layout(
    title="CPU Usage Prediction",
    xaxis_title="Time",
    yaxis_title="CPU %",
)

st.plotly_chart(
    fig,
    use_container_width=True
)
