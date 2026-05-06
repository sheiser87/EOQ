import streamlit as st
import math
from scipy import stats

st.title("Inventory Calculator")

# --- Holding Cost Calculator ---
st.header("Holding Cost Calculator")

col_h1, col_h2 = st.columns(2)
with col_h1:
    unit_cost = st.number_input("Unit Cost per Item ($)", min_value=0.0, value=10.0, step=0.50)
with col_h2:
    holding_pct = st.number_input("Annual Holding Cost (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.5)

computed_H = unit_cost * (holding_pct / 100)
st.metric("Holding Cost per Unit per Year (H)", f"${computed_H:.2f}", help="Enter this value as H in the EOQ Calculator below.")

st.divider()

# --- EOQ Calculator ---
st.header("EOQ Calculator")

col1, col2, col3 = st.columns(3)
with col1:
    R = st.number_input("Annual Demand (R)", min_value=0.0, value=10000.0, step=100.0)
with col2:
    K = st.number_input("Order Cost per Order (K)", min_value=0.0, value=50.0, step=1.0)
with col3:
    H = st.number_input("Holding Cost per Unit per Year (H)", min_value=0.01, value=2.0, step=0.1)

if H > 0:
    eoq = math.sqrt((2 * R * K) / H)
    st.metric("Economic Order Quantity (EOQ)", f"{eoq:.2f} units")
else:
    st.warning("Holding cost must be greater than zero.")

st.divider()

# --- Reorder Point Calculator ---
st.header("Reorder Point Calculator")

col4, col5, col6 = st.columns(3)
with col4:
    avg_daily_demand = st.number_input("Average Daily Demand", min_value=0.0, value=30.0, step=1.0)
with col5:
    std_daily_demand = st.number_input("Std Dev of Daily Demand", min_value=0.0, value=5.0, step=0.5)
with col6:
    lead_time = st.number_input("Lead Time (days)", min_value=0.0, value=7.0, step=1.0)

confidence = st.slider("Confidence Level", min_value=80, max_value=99, value=95, format="%d%%")

z = stats.norm.ppf(confidence / 100)
safety_stock = z * std_daily_demand * math.sqrt(lead_time)
reorder_point = (avg_daily_demand * lead_time) + safety_stock

col7, col8, col9 = st.columns(3)
with col7:
    st.metric("Z-Score", f"{z:.3f}")
with col8:
    st.metric("Safety Stock", f"{safety_stock:.2f} units")
with col9:
    st.metric("Reorder Point", f"{reorder_point:.2f} units")
