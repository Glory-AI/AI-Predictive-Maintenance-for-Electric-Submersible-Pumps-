import streamlit as st
import pandas as pd
import os
import time

CSV_PATH = "realtime_predictions.csv"

st.set_page_config(
    page_title="ESP Pump Monitor",
    page_icon="💧",
    layout="wide"
)

STATE_COLORS = {
    "NORMAL":     ("🟢", "#22c55e", "#dcfce7"),
    "DRY_RUN":    ("🟡", "#f59e0b", "#fef9c3"),
    "CAVITATION": ("🔴", "#ef4444", "#fee2e2"),
}

st.title("💧 Electric Submersible Pump — Live Monitor")
st.caption("Auto-refreshes every 2 seconds")

if not os.path.exists(CSV_PATH):
    st.warning("Waiting for data... make sure the model script is running.")
    time.sleep(2)
    st.rerun()

df = pd.read_csv(CSV_PATH)

if df.empty:
    st.warning("CSV exists but has no data yet.")
    time.sleep(2)
    st.rerun()

df["Timestamp"]    = pd.to_datetime(df["Timestamp"], format="%H:%M:%S.%f", errors="coerce")
df["Current"]        = pd.to_numeric(df["Current"],        errors="coerce")
df = df.dropna(subset=["Timestamp", "Power"]).tail(500)

power_val = float(df["Current"].iloc[-1])
state     = str(df["Predicted_State"].iloc[-1])
last_time = df["Timestamp"].iloc[-1].strftime("%H:%M:%S")

icon, color, bg = STATE_COLORS.get(state, ("⚪", "#6b7280", "#f3f4f6"))

# ── State banner ──────────────────────────────────────
st.markdown(
    f"""
    <div style="background:{bg}; border-left: 6px solid {color};
                padding: 1rem 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
        <span style="font-size:2rem; font-weight:600; color:{color};">
            {icon} {state}
        </span>
        <span style="font-size:0.85rem; color:#6b7280; margin-left:1.5rem;">
            Last reading: {last_time}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# ── Metric ────────────────────────────────────────────
st.metric("Current through pump (mA)", f"{power_val:.2f}")

st.divider()

# ── Charts ────────────────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Current through pump (mA)")
    st.line_chart(df.set_index("Timestamp")["Current"], height=280)

with col_right:
    st.subheader("State distribution")
    st.bar_chart(df["Predicted_State"].value_counts(), height=280)

st.divider()

# ── Recent predictions table ──────────────────────────
st.subheader("Recent predictions")
display_df = df[["Timestamp", "Current", "Predicted_State"]].tail(20).copy()
display_df = display_df.rename(columns={"Current": "Current (mA)"})
display_df["Timestamp"] = display_df["Timestamp"].dt.strftime("%H:%M:%S")
st.dataframe(display_df[::-1], use_container_width=True, hide_index=True)

# ── Auto rerun every 2 seconds ────────────────────────
time.sleep(2)
st.rerun()