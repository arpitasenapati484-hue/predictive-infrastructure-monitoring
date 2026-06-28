import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os, time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import CSV_PATH

# ── Page config
st.set_page_config(page_title="Infrastructure Monitor", page_icon="🖥️", layout="wide")

# ── Sidebar
with st.sidebar:
    st.title("⚙️ Controls")
    refresh_rate = st.slider("Refresh interval (sec)", 5, 60, 10)
    rows_to_show = st.slider("Data points to display", 20, 200, 60)
    st.markdown("---")
    st.caption("Predictive Infrastructure Monitor")

# ── Load data
@st.cache_data(ttl=refresh_rate)
def load_data():
    try:
        df = pd.read_csv(CSV_PATH)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
        return df.tail(200)
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

st.title("🖥️ Predictive Infrastructure Monitor")
st.caption("Live metrics · Anomaly detection · XGBoost forecasting")

if df.empty:
    st.warning("No data yet. Run `python main.py` to start collecting metrics.")
    st.stop()

recent = df.tail(rows_to_show)

# ── KPI Cards
latest = df.iloc[-1]
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧠 CPU", f"{latest['cpu_percent']:.1f}%")
col2.metric("💾 RAM", f"{latest['ram_percent']:.1f}%")
col3.metric("💿 Disk", f"{latest['disk_percent']:.1f}%")
col4.metric("📡 Net Sent", f"{latest.get('net_sent', 0)/1e6:.1f} MB")

st.markdown("---")

# ── Charts
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=("CPU %", "RAM %", "Disk %"),
    vertical_spacing=0.08,
)

metrics = [
    ("cpu_percent", "#00b4d8", 1),
    ("ram_percent", "#7b2d8b", 2),
    ("disk_percent", "#e63946", 3),
]

for col_name, color, row in metrics:
    if col_name not in recent.columns:
        continue

    fig.add_trace(
        go.Scatter(
            x=recent["timestamp"],
            y=recent[col_name],
            mode="lines",
            name=col_name.replace("_", " ").title(),
            line=dict(color=color, width=2),
        ),
        row=row, col=1,
    )

    if "is_anomaly" in recent.columns:
        anomalies = recent[recent["is_anomaly"] == True]
        fig.add_trace(
            go.Scatter(
                x=anomalies["timestamp"],
                y=anomalies[col_name],
                mode="markers",
                name="Anomaly",
                marker=dict(color="red", size=8, symbol="x"),
                showlegend=(row == 1),
            ),
            row=row, col=1,
        )

    if col_name == "cpu_percent":
        try:
            from ml.forecast import forecast_cpu
            next_val = forecast_cpu(recent.rename(columns={"cpu_percent": "cpu"}))
            if next_val is not None:
                last_time = recent["timestamp"].iloc[-1]
                fig.add_trace(
                    go.Scatter(
                        x=[last_time],
                        y=[next_val],
                        mode="markers",
                        name="CPU Forecast",
                        marker=dict(color="#00b4d8", size=12, symbol="star"),
                        showlegend=True,
                    ),
                    row=row, col=1,
                )
        except Exception:
            pass

fig.update_layout(
    height=700,
    template="plotly_dark",
    hovermode="x unified",
    margin=dict(t=40, b=20),
)
st.plotly_chart(fig, use_container_width=True)

# ── Raw data
with st.expander("📋 Raw data"):
    st.dataframe(recent.sort_values("timestamp", ascending=False), use_container_width=True)

# ── Auto-refresh
time.sleep(0.1)
st.rerun()