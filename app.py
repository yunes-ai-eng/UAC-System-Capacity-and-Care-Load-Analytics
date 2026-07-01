#code 2

# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from prophet import Prophet
# from datetime import datetime, timedelta
# import warnings
# import os
# from io import BytesIO
# from reportlab.lib.pagesizes import letter, A4
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
# from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
# import base64

# warnings.filterwarnings('ignore')

# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================
# st.set_page_config(
#     page_title="UAC System Capacity & Care Load Analytics",
#     page_icon="🏥",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS - Professional Dark Theme
# st.markdown("""
# <style>
#     .main-header { 
#         font-size: 2.8rem; 
#         font-weight: 800; 
#         color: #E2E8F0; 
#         text-align: center;
#         margin-bottom: 0.3rem;
#         letter-spacing: -0.5px;
#     }
#     .sub-header { 
#         font-size: 1.15rem; 
#         color: #94A3B8; 
#         text-align: center;
#         margin-bottom: 2.5rem;
#         font-weight: 400;
#     }
#     .kpi-card {
#         background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
#         backdrop-filter: blur(10px);
#         border: 1px solid rgba(102, 126, 234, 0.3);
#         padding: 1.8rem 1.2rem;
#         border-radius: 16px;
#         color: #E2E8F0;
#         text-align: center;
#         box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
#         transition: transform 0.3s ease;
#     }
#     .kpi-card:hover {
#         transform: translateY(-5px);
#         border-color: rgba(102, 126, 234, 0.6);
#     }
#     .kpi-value { 
#         font-size: 2.6rem; 
#         font-weight: 800;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.3rem;
#     }
#     .kpi-label { 
#         font-size: 0.85rem; 
#         color: #94A3B8;
#         text-transform: uppercase;
#         letter-spacing: 1px;
#         margin-bottom: 0.5rem;
#     }
#     .kpi-status {
#         font-size: 0.8rem;
#         padding: 0.3rem 0.8rem;
#         border-radius: 20px;
#         display: inline-block;
#         font-weight: 600;
#     }
#     .status-good { background: rgba(16, 185, 129, 0.2); color: #10B981; }
#     .status-warning { background: rgba(245, 158, 11, 0.2); color: #F59E0B; }
#     .status-danger { background: rgba(239, 68, 68, 0.2); color: #EF4444; }
#     .section-title {
#         font-size: 1.5rem;
#         font-weight: 700;
#         color: #E2E8F0;
#         margin-top: 2.5rem;
#         margin-bottom: 1.2rem;
#         padding-left: 1.2rem;
#         border-left: 4px solid #667eea;
#     }
#     .section-subtitle {
#         font-size: 0.95rem;
#         color: #64748B;
#         margin-bottom: 1.5rem;
#         padding-left: 1.2rem;
#     }
#     .alert-box { 
#         padding: 1.2rem; 
#         border-radius: 12px; 
#         margin: 1rem 0; 
#         border-left: 4px solid;
#         background: rgba(15, 23, 42, 0.8);
#     }
#     .alert-danger { border-color: #EF4444; }
#     .alert-warning { border-color: #F59E0B; }
#     .alert-success { border-color: #10B981; }
#     .alert-info { border-color: #3B82F6; }
#     .insight-card {
#         background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
#         border: 1px solid rgba(16, 185, 129, 0.2);
#         padding: 1.5rem;
#         border-radius: 12px;
#         margin: 1rem 0;
#     }
#     .stress-meter {
#         height: 8px;
#         border-radius: 4px;
#         background: linear-gradient(90deg, #10B981 0%, #F59E0B 50%, #EF4444 100%);
#         position: relative;
#     }
#     .stress-marker {
#         width: 4px;
#         height: 16px;
#         background: white;
#         position: absolute;
#         top: -4px;
#         border-radius: 2px;
#         box-shadow: 0 0 10px rgba(255,255,255,0.5);
#     }
#     .auto-alert {
#         animation: pulse 2s infinite;
#     }
#     @keyframes pulse {
#         0% { opacity: 1; }
#         50% { opacity: 0.7; }
#         100% { opacity: 1; }
#     }
# </style>
# """, unsafe_allow_html=True)

# # ============================================================
# # HEADER
# # ============================================================
# st.markdown('<div class="main-header">🏥 System Capacity & Care Load Analytics</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-header">Unaccompanied Children (UAC) Program | Real-Time Capacity Monitoring & Stress Detection</div>', unsafe_allow_html=True)

# # ============================================================
# # LOAD DATA
# # ============================================================
# @st.cache_data(ttl=3600)
# def load_data():
#     possible_paths = [
#         "data/HHS_Unaccompanied_Alien_Children_Program.csv",
#         "../data/HHS_Unaccompanied_Alien_Children_Program.csv",
#         "HHS_Unaccompanied_Alien_Children_Program.csv",
#         "data/uac_capacity_data.csv",
#         "../data/uac_capacity_data.csv"
#     ]
    
#     df = None
#     used_path = None
    
#     for path in possible_paths:
#         if os.path.exists(path):
#             try:
#                 df = pd.read_csv(path)
#                 used_path = path
#                 break
#             except Exception:
#                 continue
    
#     if df is not None:
#         st.success(f"✅ Data loaded from: {used_path}")
        
#         # FIXED: More precise column mapping - check more specific names FIRST
#         col_mapping = {}
#         for col in df.columns:
#             col_lower = col.lower().strip()
#             if 'date' in col_lower:
#                 col_mapping[col] = 'date'
#             elif 'transferred out' in col_lower:
#                 col_mapping[col] = 'transferred'
#             elif 'discharged' in col_lower:
#                 col_mapping[col] = 'discharged'
#             elif 'apprehended' in col_lower or 'placed in cbp' in col_lower:
#                 col_mapping[col] = 'apprehended'
#             elif 'in cbp' in col_lower or 'cbp custody' in col_lower:
#                 col_mapping[col] = 'in_cbp'
#             elif 'in hhs' in col_lower or 'hhs care' in col_lower:
#                 col_mapping[col] = 'in_hhs'
        
#         df = df.rename(columns=col_mapping)
#         df["date"] = pd.to_datetime(df["date"])
        
#         # Remove duplicate columns if any
#         if df.columns.duplicated().any():
#             df = df.loc[:, ~df.columns.duplicated()]
        
#         # Convert numeric columns safely
#         for col in ["apprehended", "in_cbp", "transferred", "in_hhs", "discharged"]:
#             if col in df.columns:
#                 df[col] = df[col].apply(
#                     lambda x: pd.to_numeric(str(x).replace(',', '').replace('$', '').strip(), errors='coerce')
#                 )
        
#         required_cols = ["date", "apprehended", "in_cbp", "transferred", "in_hhs", "discharged"]
#         available_cols = [c for c in required_cols if c in df.columns]
        
#         df = df[available_cols].dropna().sort_values("date").reset_index(drop=True)
#         return df
    
#     # Generate realistic synthetic data
#     st.info("📊 Using synthetic data for demonstration...")
#     dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq="D")
#     np.random.seed(42)
#     n_days = len(dates)
    
#     day_of_year = dates.dayofyear
#     seasonal = 1 + 0.35 * np.sin(2 * np.pi * (day_of_year - 60) / 365)
#     policy_effect = np.ones(n_days)
#     policy_effect[400:450] = 0.6
#     policy_effect[700:750] = 1.4
    
#     trend = np.linspace(1.0, 1.2, n_days)
    
#     base_intake = (120 * seasonal * trend * policy_effect + np.random.normal(0, 20, n_days)).astype(int)
#     base_intake = np.maximum(base_intake, 15)
    
#     cbp = np.zeros(n_days)
#     cbp[0] = base_intake[0]
#     for i in range(1, n_days):
#         outflow = int(cbp[i-1] * np.random.uniform(0.2, 0.4))
#         cbp[i] = max(0, min(2500, cbp[i-1] + base_intake[i] - outflow))
    
#     transfers = np.minimum(
#         (cbp * np.random.uniform(0.5, 0.85, n_days) + np.random.normal(0, 8, n_days)).astype(int),
#         cbp
#     )
#     transfers = np.maximum(transfers, 0)
    
#     hhs = np.zeros(n_days)
#     hhs[0] = transfers[0]
#     for i in range(1, n_days):
#         discharge_rate = np.random.uniform(0.06, 0.2)
#         discharges_today = int(hhs[i-1] * discharge_rate)
#         hhs[i] = max(0, hhs[i-1] + transfers[i] - discharges_today)
    
#     discharges = np.zeros(n_days)
#     for i in range(1, n_days):
#         discharge_rate = np.random.uniform(0.06, 0.2)
#         discharges[i] = int(hhs[i-1] * discharge_rate)
#     discharges = np.minimum(discharges, hhs)
    
#     df = pd.DataFrame({
#         "date": dates,
#         "apprehended": base_intake.astype(int),
#         "in_cbp": cbp.astype(int),
#         "transferred": transfers.astype(int),
#         "in_hhs": hhs.astype(int),
#         "discharged": discharges.astype(int)
#     })
#     return df

# df = load_data()

# # ============================================================
# # BACKEND LOGIC - DERIVED HEALTHCARE CAPACITY METRICS
# # ============================================================

# df["Total_System_Load"] = df["in_cbp"] + df["in_hhs"]
# df["Net_Daily_Intake"] = df["transferred"] - df["discharged"]
# df["Growth_Rate"] = df["Total_System_Load"].pct_change() * 100

# df["Load_Rolling_7d"] = df["Total_System_Load"].rolling(window=7, min_periods=1).mean()
# df["Load_Rolling_14d"] = df["Total_System_Load"].rolling(window=14, min_periods=1).mean()
# df["CBP_Rolling_7d"] = df["in_cbp"].rolling(window=7, min_periods=1).mean()
# df["CBP_Rolling_14d"] = df["in_cbp"].rolling(window=14, min_periods=1).mean()
# df["HHS_Rolling_7d"] = df["in_hhs"].rolling(window=7, min_periods=1).mean()
# df["HHS_Rolling_14d"] = df["in_hhs"].rolling(window=14, min_periods=1).mean()

# df["Backlog_7d"] = df["Net_Daily_Intake"].rolling(window=7, min_periods=1).sum()
# df["Backlog_14d"] = df["Net_Daily_Intake"].rolling(window=14, min_periods=1).sum()

# df["Load_Volatility"] = df["Total_System_Load"].rolling(window=14, min_periods=1).std()
# df["CBP_Volatility"] = df["in_cbp"].rolling(window=7, min_periods=1).std()
# df["HHS_Volatility"] = df["in_hhs"].rolling(window=7, min_periods=1).std()

# df["Stress_Flag"] = df["Total_System_Load"] > df["Load_Rolling_14d"] * 1.1
# df["Sustained_Stress"] = df["Stress_Flag"].rolling(window=7, min_periods=1).sum()

# df["KPI_Total_Load"] = df["Total_System_Load"]
# df["KPI_Net_Intake"] = df["Net_Daily_Intake"].rolling(window=7, min_periods=1).mean()
# df["KPI_Volatility"] = (df["Load_Volatility"] / df["Total_System_Load"].rolling(window=14, min_periods=1).mean()) * 100
# df["KPI_Backlog_Rate"] = df["Backlog_14d"] / 14
# df["KPI_Discharge_Ratio"] = df["discharged"] / df["transferred"].replace(0, np.nan)

# df = df.fillna(0)

# # ============================================================
# # SIDEBAR - CONTROL PANEL
# # ============================================================
# st.sidebar.markdown("## ⚙️ Control Panel")
# st.sidebar.markdown("---")

# min_date = df["date"].min().date()
# max_date = df["date"].max().date()

# col1, col2 = st.sidebar.columns(2)
# with col1:
#     start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
# with col2:
#     end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# mask = (df["date"] >= pd.Timestamp(start_date)) & (df["date"] <= pd.Timestamp(end_date))
# filtered_df = df[mask].copy()

# st.sidebar.markdown("---")

# granularity = st.sidebar.selectbox("⏱️ Time Granularity", ["Daily", "Weekly", "Monthly"], index=0)

# if granularity == "Weekly":
#     filtered_df = filtered_df.set_index("date").resample("W").mean().reset_index()
#     filtered_df["date"] = filtered_df["date"].dt.to_period("W").dt.start_time
# elif granularity == "Monthly":
#     filtered_df = filtered_df.set_index("date").resample("M").mean().reset_index()
#     filtered_df["date"] = filtered_df["date"].dt.to_period("M").dt.start_time

# st.sidebar.markdown("---")
# st.sidebar.markdown("### 📊 Display Options")
# show_cbp = st.sidebar.checkbox("Show CBP Load", value=True)
# show_hhs = st.sidebar.checkbox("Show HHS Load", value=True)
# show_total = st.sidebar.checkbox("Show Total System Load", value=True)
# show_rolling = st.sidebar.checkbox("Show Rolling Averages", value=True)
# show_stress = st.sidebar.checkbox("Highlight Stress Periods", value=True)

# st.sidebar.markdown("---")
# st.sidebar.markdown("### 🔮 Forecast")
# forecast_days = st.sidebar.slider("Forecast Days", 30, 365, 90)

# st.sidebar.markdown("---")
# st.sidebar.markdown("### 🔔 Auto Alerts")
# alert_threshold = st.sidebar.number_input("Capacity Alert Threshold", min_value=1000, max_value=20000, value=8000)
# enable_alerts = st.sidebar.checkbox("Enable Auto Alerts", value=True)

# st.sidebar.markdown("---")
# st.sidebar.markdown("### 📅 Period Comparison")
# compare_periods = st.sidebar.checkbox("Compare Two Periods", value=False)
# if compare_periods:
#     st.sidebar.markdown("**Period 1 (Current)**")
#     p1_start = st.sidebar.date_input("P1 Start", min_date, min_value=min_date, max_value=max_date)
#     p1_end = st.sidebar.date_input("P1 End", min_date + timedelta(days=90), min_value=min_date, max_value=max_date)
#     st.sidebar.markdown("**Period 2 (Compare)**")
#     p2_start = st.sidebar.date_input("P2 Start", max_date - timedelta(days=180), min_value=min_date, max_value=max_date)
#     p2_end = st.sidebar.date_input("P2 End", max_date, min_value=min_date, max_value=max_date)

# # ============================================================
# # AUTO ALERTS SECTION
# # ============================================================
# if enable_alerts:
#     latest = filtered_df.iloc[-1] if len(filtered_df) > 0 else df.iloc[-1]
    
#     alerts = []
#     if latest["Total_System_Load"] > alert_threshold:
#         alerts.append(("🚨 CAPACITY ALERT", f"System load ({int(latest['Total_System_Load'])}) exceeds threshold ({alert_threshold})", "danger"))
#     if latest["Sustained_Stress"] >= 5:
#         alerts.append(("🔥 STRESS ALERT", f"Sustained stress for {int(latest['Sustained_Stress'])} days", "danger"))
#     if latest["Backlog_14d"] > 100:
#         alerts.append(("📈 BACKLOG ALERT", f"14-day backlog accumulation: {int(latest['Backlog_14d'])}", "warning"))
#     if latest["KPI_Net_Intake"] > 50:
#         alerts.append(("⚠️ INTAKE PRESSURE", f"High net intake: {latest['KPI_Net_Intake']:.1f} children/day", "warning"))
    
#     if alerts:
#         st.markdown("---")
#         st.markdown('<div class="section-title">🚨 Active Alerts</div>', unsafe_allow_html=True)
#         for title, message, level in alerts:
#             color = "#EF4444" if level == "danger" else "#F59E0B"
#             st.markdown(f"""
#             <div style="background: linear-gradient(135deg, rgba({','.join(['239', '68', '68'] if level == 'danger' else ['245', '158', '11'])}, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%);
#                         border-left: 4px solid {color}; padding: 1rem 1.5rem; border-radius: 12px; margin: 0.5rem 0;">
#                 <strong style="color: {color}; font-size: 1.1rem;">{title}</strong>
#                 <p style="color: #E2E8F0; margin: 0.3rem 0 0 0;">{message}</p>
#             </div>
#             """, unsafe_allow_html=True)

# # ============================================================
# # LATEST DATA FOR KPIs
# # ============================================================
# latest = filtered_df.iloc[-1] if len(filtered_df) > 0 else df.iloc[-1]

# stress_level = latest["Sustained_Stress"]
# if stress_level >= 5:
#     stress_status = "CRITICAL"
#     stress_class = "status-danger"
# elif stress_level >= 3:
#     stress_status = "ELEVATED"
#     stress_class = "status-warning"
# else:
#     stress_status = "NORMAL"
#     stress_class = "status-good"

# backlog_trend = latest["Backlog_14d"]
# if backlog_trend > 50:
#     backlog_status = "ACCUMULATING"
#     backlog_class = "status-danger"
# elif backlog_trend > 0:
#     backlog_status = "GROWING"
#     backlog_class = "status-warning"
# else:
#     backlog_status = "STABLE"
#     backlog_class = "status-good"

# # ============================================================
# # SECTION 1: KPI SUMMARY CARDS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">📊 System Capacity Overview</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">Real-time monitoring of total care load, intake pressure, and system stress levels</div>', unsafe_allow_html=True)

# kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

# with kpi_col1:
#     total_load = int(latest["KPI_Total_Load"])
#     st.markdown(f"""
#     <div class="kpi-card">
#         <div class="kpi-value">{total_load:,}</div>
#         <div class="kpi-label">Total Children Under Care</div>
#         <div class="kpi-status {stress_class}">{stress_status}</div>
#     </div>
#     """, unsafe_allow_html=True)

# with kpi_col2:
#     daily_intake = int(latest["transferred"])
#     st.markdown(f"""
#     <div class="kpi-card">
#         <div class="kpi-value">{daily_intake:,}</div>
#         <div class="kpi-label">Daily Intake (Transfers)</div>
#         <div class="kpi-status status-info">Into HHS System</div>
#     </div>
#     """, unsafe_allow_html=True)

# with kpi_col3:
#     daily_outflow = int(latest["discharged"])
#     st.markdown(f"""
#     <div class="kpi-card">
#         <div class="kpi-value">{daily_outflow:,}</div>
#         <div class="kpi-label">Daily Outflow (Discharges)</div>
#         <div class="kpi-status status-info">To Sponsors</div>
#     </div>
#     """, unsafe_allow_html=True)

# with kpi_col4:
#     net_intake = latest["KPI_Net_Intake"]
#     pressure_color = "status-danger" if net_intake > 10 else "status-warning" if net_intake > 0 else "status-good"
#     pressure_text = "HIGH PRESSURE" if net_intake > 10 else "MODERATE" if net_intake > 0 else "BALANCED"
#     st.markdown(f"""
#     <div class="kpi-card">
#         <div class="kpi-value">{net_intake:+.0f}</div>
#         <div class="kpi-label">Net Intake Pressure</div>
#         <div class="kpi-status {pressure_color}">{pressure_text}</div>
#     </div>
#     """, unsafe_allow_html=True)

# # ============================================================
# # STRESS METER
# # ============================================================
# st.markdown("---")
# stress_col1, stress_col2 = st.columns([3, 1])

# with stress_col1:
#     st.markdown('<div class="section-title">🔥 System Stress Indicator</div>', unsafe_allow_html=True)
#     current_stress = min(stress_level / 7 * 100, 100)
#     st.markdown(f"""
#     <div style="background: rgba(15, 23, 42, 0.8); padding: 1.5rem; border-radius: 12px;">
#         <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
#             <span style="color: #10B981; font-weight: 600;">Normal</span>
#             <span style="color: #F59E0B; font-weight: 600;">Elevated</span>
#             <span style="color: #EF4444; font-weight: 600;">Critical</span>
#         </div>
#         <div class="stress-meter">
#             <div class="stress-marker" style="left: {current_stress}%;"></div>
#         </div>
#         <div style="text-align: center; margin-top: 1rem; color: #94A3B8;">
#             Current Stress Level: <strong style="color: {'#EF4444' if stress_level >= 5 else '#F59E0B' if stress_level >= 3 else '#10B981'};">{stress_level}/7 days</strong> sustained pressure
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# with stress_col2:
#     st.markdown('<div class="section-title">📈 Backlog Trend</div>', unsafe_allow_html=True)
#     st.markdown(f"""
#     <div style="background: rgba(15, 23, 42, 0.8); padding: 1.5rem; border-radius: 12px; text-align: center;">
#         <div style="font-size: 2.2rem; font-weight: 800; color: {'#EF4444' if backlog_trend > 50 else '#F59E0B' if backlog_trend > 0 else '#10B981'};">{backlog_trend:+.0f}</div>
#         <div style="color: #94A3B8; font-size: 0.9rem;">14-Day Accumulation</div>
#         <div class="kpi-status {backlog_class}" style="margin-top: 0.8rem;">{backlog_status}</div>
#     </div>
#     """, unsafe_allow_html=True)

# # ============================================================
# # SECTION 2: TIME SERIES ANALYSIS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">📈 Time Series Analysis: System Load & Pressure Detection</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">When the daily load (solid line) rises above the 14-day rolling average (dashed), the system enters a stress period</div>', unsafe_allow_html=True)

# fig_load = go.Figure()

# if show_total:
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["Total_System_Load"],
#         mode="lines", name="Total System Load",
#         line=dict(color="#667eea", width=2),
#         fill="tozeroy", fillcolor="rgba(102, 126, 234, 0.08)",
#         hovertemplate="<b>Total Load</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>"
#     ))

# if show_cbp:
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["in_cbp"],
#         mode="lines", name="CBP Custody",
#         line=dict(color="#f5576c", width=1.5),
#         hovertemplate="<b>CBP</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>"
#     ))

# if show_hhs:
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["in_hhs"],
#         mode="lines", name="HHS Care",
#         line=dict(color="#11998e", width=1.5),
#         hovertemplate="<b>HHS</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>"
#     ))

# if show_rolling:
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["Load_Rolling_7d"],
#         mode="lines", name="7-Day Rolling Avg",
#         line=dict(color="#F59E0B", width=2, dash="dash"),
#         hovertemplate="<b>7-Day Avg</b><br>Date: %{x}<br>Avg: %{y:,.0f}<extra></extra>"
#     ))
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["Load_Rolling_14d"],
#         mode="lines", name="14-Day Rolling Avg",
#         line=dict(color="#EF4444", width=2, dash="dot"),
#         hovertemplate="<b>14-Day Avg</b><br>Date: %{x}<br>Avg: %{y:,.0f}<extra></extra>"
#     ))

# if show_stress:
#     stress_df = filtered_df[filtered_df["Stress_Flag"] == True]
#     if len(stress_df) > 0:
#         fig_load.add_trace(go.Scatter(
#             x=stress_df["date"], y=stress_df["Total_System_Load"],
#             mode="markers", name="⚠️ Stress Period",
#             marker=dict(color="#EF4444", size=8, symbol="diamond"),
#             hovertemplate="<b>STRESS ALERT</b><br>Date: %{x}<br>Load: %{y:,.0f}<extra></extra>"
#         ))

# # Add alert threshold line
# if enable_alerts:
#     fig_load.add_hline(y=alert_threshold, line_dash="dash", line_color="#EF4444", opacity=0.7,
#                         annotation_text=f"Alert ({alert_threshold})", annotation_position="top right")

# fig_load.update_layout(
#     height=500,
#     template="plotly_dark",
#     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#     yaxis_title="Number of Children",
#     xaxis_title="Date",
#     hovermode="x unified"
# )

# st.plotly_chart(fig_load, use_container_width=True)

# # ============================================================
# # SECTION 3: PERIOD COMPARISON (NEW FEATURE)
# # ============================================================
# if compare_periods:
#     st.markdown("---")
#     st.markdown('<div class="section-title">📅 Period Comparison Analysis</div>', unsafe_allow_html=True)
#     st.markdown('<div class="section-subtitle">Compare capacity metrics between two time periods</div>', unsafe_allow_html=True)
    
#     p1_mask = (df["date"] >= pd.Timestamp(p1_start)) & (df["date"] <= pd.Timestamp(p1_end))
#     p2_mask = (df["date"] >= pd.Timestamp(p2_start)) & (df["date"] <= pd.Timestamp(p2_end))
#     p1_df = df[p1_mask]
#     p2_df = df[p2_mask]
    
#     if len(p1_df) > 0 and len(p2_df) > 0:
#         comp_metrics = {
#             "Metric": ["Avg Total Load", "Avg CBP Load", "Avg HHS Load", "Avg Transfers", "Avg Discharges", "Peak Load", "Stress Days"],
#             f"Period 1 ({p1_start} to {p1_end})": [
#                 f"{p1_df['Total_System_Load'].mean():.0f}",
#                 f"{p1_df['in_cbp'].mean():.0f}",
#                 f"{p1_df['in_hhs'].mean():.0f}",
#                 f"{p1_df['transferred'].mean():.0f}",
#                 f"{p1_df['discharged'].mean():.0f}",
#                 f"{p1_df['Total_System_Load'].max():.0f}",
#                 f"{p1_df['Stress_Flag'].sum():.0f}"
#             ],
#             f"Period 2 ({p2_start} to {p2_end})": [
#                 f"{p2_df['Total_System_Load'].mean():.0f}",
#                 f"{p2_df['in_cbp'].mean():.0f}",
#                 f"{p2_df['in_hhs'].mean():.0f}",
#                 f"{p2_df['transferred'].mean():.0f}",
#                 f"{p2_df['discharged'].mean():.0f}",
#                 f"{p2_df['Total_System_Load'].max():.0f}",
#                 f"{p2_df['Stress_Flag'].sum():.0f}"
#             ],
#             "Change": [
#                 f"{((p2_df['Total_System_Load'].mean() - p1_df['Total_System_Load'].mean()) / p1_df['Total_System_Load'].mean() * 100):+.1f}%",
#                 f"{((p2_df['in_cbp'].mean() - p1_df['in_cbp'].mean()) / p1_df['in_cbp'].mean() * 100):+.1f}%",
#                 f"{((p2_df['in_hhs'].mean() - p1_df['in_hhs'].mean()) / p1_df['in_hhs'].mean() * 100):+.1f}%",
#                 f"{((p2_df['transferred'].mean() - p1_df['transferred'].mean()) / p1_df['transferred'].mean() * 100):+.1f}%",
#                 f"{((p2_df['discharged'].mean() - p1_df['discharged'].mean()) / p1_df['discharged'].mean() * 100):+.1f}%",
#                 f"{((p2_df['Total_System_Load'].max() - p1_df['Total_System_Load'].max()) / p1_df['Total_System_Load'].max() * 100):+.1f}%",
#                 f"{p2_df['Stress_Flag'].sum() - p1_df['Stress_Flag'].sum():+.0f}"
#             ]
#         }
#         st.dataframe(pd.DataFrame(comp_metrics), use_container_width=True, hide_index=True)
        
#         # Comparison chart
#         fig_comp = go.Figure()
#         fig_comp.add_trace(go.Bar(
#             x=["Total Load", "CBP", "HHS", "Transfers", "Discharges"],
#             y=[p1_df['Total_System_Load'].mean(), p1_df['in_cbp'].mean(), p1_df['in_hhs'].mean(), 
#                p1_df['transferred'].mean(), p1_df['discharged'].mean()],
#             name=f"Period 1", marker_color="#667eea"
#         ))
#         fig_comp.add_trace(go.Bar(
#             x=["Total Load", "CBP", "HHS", "Transfers", "Discharges"],
#             y=[p2_df['Total_System_Load'].mean(), p2_df['in_cbp'].mean(), p2_df['in_hhs'].mean(),
#                p2_df['transferred'].mean(), p2_df['discharged'].mean()],
#             name=f"Period 2", marker_color="#10B981"
#         ))
#         fig_comp.update_layout(
#             height=400, template="plotly_dark", barmode="group",
#             title="Average Metrics Comparison"
#         )
#         st.plotly_chart(fig_comp, use_container_width=True)

# # ============================================================
# # SECTION 4: SYSTEM BALANCE
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">⚖️ System Balance: Intake vs Discharge Gap</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">Persistent positive gap indicates backlog accumulation and capacity strain</div>', unsafe_allow_html=True)

# fig_balance = make_subplots(
#     rows=2, cols=1,
#     subplot_titles=("Net Daily Intake (Transfers - Discharges)", "14-Day Backlog Accumulation Trend"),
#     vertical_spacing=0.15
# )

# colors = ["#10B981" if x < 0 else "#EF4444" if x > 10 else "#F59E0B" for x in filtered_df["Net_Daily_Intake"]]
# fig_balance.add_trace(go.Bar(
#     x=filtered_df["date"], y=filtered_df["Net_Daily_Intake"],
#     name="Net Intake", marker_color=colors, opacity=0.8,
#     hovertemplate="<b>Net Intake</b><br>Date: %{x}<br>Value: %{y:+.0f}<extra></extra>"
# ), row=1, col=1)

# fig_balance.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
# fig_balance.add_hline(y=10, line_dash="dot", line_color="#EF4444", row=1, col=1,
#                        annotation_text="Critical Threshold", annotation_position="top right")

# fig_balance.add_trace(go.Scatter(
#     x=filtered_df["date"], y=filtered_df["Backlog_14d"],
#     mode="lines", name="14-Day Backlog", fill="tozeroy",
#     line=dict(color="#667eea", width=2),
#     fillcolor="rgba(102, 126, 234, 0.15)",
#     hovertemplate="<b>14-Day Backlog</b><br>Date: %{x}<br>Accumulation: %{y:+.0f}<extra></extra>"
# ), row=2, col=1)

# fig_balance.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)

# fig_balance.update_layout(
#     height=650,
#     template="plotly_dark",
#     showlegend=True,
#     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
# )

# st.plotly_chart(fig_balance, use_container_width=True)

# # ============================================================
# # SECTION 5: PRESSURE & STRESS IDENTIFICATION
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">🔍 Pressure & Stress Identification</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">Rolling averages and variability analysis to detect prolonged strain windows</div>', unsafe_allow_html=True)

# fig_stress = make_subplots(
#     rows=2, cols=2,
#     subplot_titles=(
#         "CBP: 7-Day vs 14-Day Rolling Average",
#         "HHS: 7-Day vs 14-Day Rolling Average",
#         "CBP Load Variability (7d Std Dev)",
#         "HHS Load Variability (7d Std Dev)"
#     ),
#     vertical_spacing=0.12, horizontal_spacing=0.08
# )

# fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["CBP_Rolling_7d"], 
#                mode="lines", name="CBP 7d", line=dict(color="#f5576c")), row=1, col=1)
# fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["CBP_Rolling_14d"], 
#                mode="lines", name="CBP 14d", line=dict(color="#f093fb", dash="dash")), row=1, col=1)

# fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["HHS_Rolling_7d"], 
#                mode="lines", name="HHS 7d", line=dict(color="#11998e")), row=1, col=2)
# fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["HHS_Rolling_14d"], 
#                mode="lines", name="HHS 14d", line=dict(color="#38ef7d", dash="dash")), row=1, col=2)

# fig_stress.add_trace(go.Bar(x=filtered_df["date"], y=filtered_df["CBP_Volatility"], 
#            marker_color="#f5576c", opacity=0.6, name="CBP Volatility"), row=2, col=1)
# fig_stress.add_trace(go.Bar(x=filtered_df["date"], y=filtered_df["HHS_Volatility"], 
#            marker_color="#11998e", opacity=0.6, name="HHS Volatility"), row=2, col=2)

# fig_stress.update_layout(height=650, template="plotly_dark", showlegend=False)
# st.plotly_chart(fig_stress, use_container_width=True)

# # ============================================================
# # SECTION 6: CAPACITY DISTRIBUTION & FLOW
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">🏛️ Capacity Distribution & Flow Analysis</div>', unsafe_allow_html=True)

# fig_dist = make_subplots(
#     rows=1, cols=2,
#     specs=[[{"type": "pie"}, {"type": "xy"}]],
#     subplot_titles=("Current Load Distribution", "Transfer vs Discharge Flow")
# )

# latest_data = filtered_df.iloc[-1] if len(filtered_df) > 0 else df.iloc[-1]

# fig_dist.add_trace(go.Pie(
#     labels=["CBP Custody", "HHS Care"],
#     values=[latest_data["in_cbp"], latest_data["in_hhs"]],
#     hole=0.55,
#     marker_colors=["#f5576c", "#11998e"],
#     textinfo="label+percent",
#     textfont=dict(size=12, color="white")
# ), row=1, col=1)

# fig_dist.add_trace(go.Scatter(
#     x=filtered_df["date"], y=filtered_df["transferred"],
#     mode="lines", name="Transfers to HHS", line=dict(color="#667eea", width=2),
#     fill="tozeroy", fillcolor="rgba(102, 126, 234, 0.15)"
# ), row=1, col=2)

# fig_dist.add_trace(go.Scatter(
#     x=filtered_df["date"], y=filtered_df["discharged"],
#     mode="lines", name="Discharges from HHS", line=dict(color="#10B981", width=2),
#     fill="tozeroy", fillcolor="rgba(16, 185, 129, 0.15)"
# ), row=1, col=2)

# fig_dist.update_layout(height=400, template="plotly_dark", showlegend=True,
#                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
# st.plotly_chart(fig_dist, use_container_width=True)

# # ============================================================
# # SECTION 7: AI FORECASTING (IMPROVED PROPHET)
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">🔮 AI Forecasting: Total System Load Prediction</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">Prophet model with changepoint detection for policy shift awareness</div>', unsafe_allow_html=True)

# prophet_df = filtered_df[["date", "Total_System_Load"]].rename(columns={"date": "ds", "Total_System_Load": "y"})

# # IMPROVED: Better changepoint handling for policy shifts
# model = Prophet(
#     yearly_seasonality=True,
#     weekly_seasonality=True,
#     daily_seasonality=False,
#     changepoint_prior_scale=0.15,  # Increased for better policy shift detection
#     seasonality_prior_scale=10.0,
#     holidays_prior_scale=15.0,
#     growth="flat",
#     changepoint_range=0.95  # Allow changepoints up to 95% of data
# )

# # Add custom changepoints for known policy periods
# if len(prophet_df) > 365:
#     model.add_seasonality(name="monthly", period=30.5, fourier_order=5)

# # Add holiday effects for known policy changes
# policy_changes = pd.DataFrame({
#     'holiday': 'policy_change',
#     'ds': pd.to_datetime(['2024-03-01', '2024-09-01', '2025-01-01']),
#     'lower_window': -15,
#     'upper_window': 15
# })
# model = Prophet(
#     yearly_seasonality=True,
#     weekly_seasonality=True,
#     daily_seasonality=False,
#     changepoint_prior_scale=0.15,
#     seasonality_prior_scale=10.0,
#     holidays=policy_changes,
#     growth="flat",
#     changepoint_range=0.95
# )

# if len(prophet_df) > 365:
#     model.add_seasonality(name="monthly", period=30.5, fourier_order=5)

# model.fit(prophet_df)

# future = model.make_future_dataframe(periods=forecast_days)
# future["floor"] = 0  # Ensure non-negative

# forecast = model.predict(future)

# # Better bounds handling
# forecast["yhat"] = np.maximum(forecast["yhat"], 0)
# forecast["yhat_lower"] = np.maximum(forecast["yhat_lower"], 0)
# forecast["yhat_upper"] = np.maximum(forecast["yhat_upper"], 0)

# fig_forecast = go.Figure()
# fig_forecast.add_trace(go.Scatter(
#     x=prophet_df["ds"], y=prophet_df["y"],
#     name="Actual Load", mode="lines", line=dict(color="#3B82F6", width=2)
# ))
# fig_forecast.add_trace(go.Scatter(
#     x=forecast["ds"], y=forecast["yhat"],
#     name="AI Forecast", mode="lines", line=dict(color="#10B981", width=2)
# ))
# fig_forecast.add_trace(go.Scatter(
#     x=forecast["ds"].tolist() + forecast["ds"].tolist()[::-1],
#     y=forecast["yhat_upper"].tolist() + forecast["yhat_lower"].tolist()[::-1],
#     fill="toself", fillcolor="rgba(16, 185, 129, 0.15)",
#     line=dict(color="rgba(255,255,255,0)"), name="Confidence Interval"
# ))

# # Capacity threshold
# fig_forecast.add_hline(y=alert_threshold, line_dash="dash", line_color="#EF4444",
#                         annotation_text=f"Alert ({alert_threshold})", annotation_position="top right")

# fig_forecast.update_layout(
#     title=f"Forecast for Total System Load ({forecast_days} days)",
#     yaxis_title="Total Children Under Care",
#     height=500, template="plotly_dark", hovermode="x unified"
# )
# st.plotly_chart(fig_forecast, use_container_width=True)

# # Forecast insights
# future_value = forecast["yhat"].iloc[-1]
# recent_value = forecast["yhat"].iloc[-forecast_days] if len(forecast) > forecast_days else forecast["yhat"].iloc[len(forecast)//2]
# trend_change = ((future_value - recent_value) / recent_value * 100) if recent_value > 0 else 0

# insight_col1, insight_col2, insight_col3 = st.columns(3)
# with insight_col1:
#     if trend_change > 10:
#         st.error(f"🚨 Capacity Crisis\n+{trend_change:.1f}% predicted")
#     elif trend_change > 0:
#         st.warning(f"⚠️ Growing Load\n+{trend_change:.1f}% predicted")
#     else:
#         st.success(f"✅ Capacity Relief\n{trend_change:.1f}% predicted")

# with insight_col2:
#     peak_date = forecast.loc[forecast["yhat"].idxmax(), "ds"]
#     st.info(f"📅 Predicted Peak\n{peak_date.strftime('%B %Y')}")

# with insight_col3:
#     conf_width = (forecast["yhat_upper"].iloc[-1] - forecast["yhat_lower"].iloc[-1]) / forecast["yhat"].iloc[-1] * 100
#     st.success(f"✅ Confidence\n±{conf_width/2:.1f}% uncertainty")

# # ============================================================
# # SECTION 8: DATA QUALITY & ANOMALIES (FIXED LOGIC)
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">🔍 Data Quality & Logical Constraint Validation</div>', unsafe_allow_html=True)

# violations = []
# for idx, row in filtered_df.iterrows():
#     # FIXED: More realistic validation - transfers should not exceed those available in CBP
#     # But daily transfers CAN exceed current CBP if CBP has been accumulating
#     # Better check: transfers should not exceed (in_cbp + transferred) which represents total flow
#     if row["transferred"] > (row["in_cbp"] + row["transferred"]):
#         violations.append({"Date": row["date"], "Type": "Transfer exceeds total CBP flow", "Severity": "Critical"})
#     # Discharges should not exceed current HHS care
#     if row["discharged"] > row["in_hhs"]:
#         violations.append({"Date": row["date"], "Type": "Discharge > HHS Care", "Severity": "Critical"})
#     # Check for negative values
#     if any(row[col] < 0 for col in ["in_cbp", "in_hhs", "transferred", "discharged"]):
#         violations.append({"Date": row["date"], "Type": "Negative value detected", "Severity": "Warning"})
#     # Check for extreme outliers (more than 3 std dev)
#     if row["Total_System_Load"] > (df["Total_System_Load"].mean() + 3 * df["Total_System_Load"].std()):
#         violations.append({"Date": row["date"], "Type": "Extreme outlier load", "Severity": "Warning"})

# if violations:
#     st.warning(f"⚠️ {len(violations)} data quality issues detected")
#     st.dataframe(pd.DataFrame(violations), use_container_width=True)
# else:
#     st.success("✅ All logical constraints validated successfully")

# # ============================================================
# # SECTION 9: EXECUTIVE INSIGHTS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">💡 Executive Insights & Recommendations</div>', unsafe_allow_html=True)

# stress_periods = []
# in_stress = False
# start_date_stress = None
# for idx, row in filtered_df.iterrows():
#     if row["Stress_Flag"] and not in_stress:
#         in_stress = True
#         start_date_stress = row["date"]
#     elif not row["Stress_Flag"] and in_stress:
#         in_stress = False
#         if start_date_stress:
#             duration = (row["date"] - start_date_stress).days if hasattr(row["date"], 'days') else 1
#             if duration >= 3:
#                 stress_periods.append(f"{start_date_stress.strftime('%Y-%m-%d')} to {row['date'].strftime('%Y-%m-%d')} ({duration} days)")

# sustained_backlog = filtered_df[filtered_df["Backlog_14d"] > 50]
# has_backlog = len(sustained_backlog) > 7

# st.markdown(f"""
# <div class="insight-card">
#     <h4 style="color: #E2E8F0; margin-bottom: 1rem;">🎯 Key Findings</h4>
#     <ul style="color: #CBD5E1; line-height: 2;">
#         <li><strong>System Load:</strong> Currently <span style="color: {'#EF4444' if total_load > alert_threshold else '#10B981'};">{total_load:,} children</span> under care</li>
#         <li><strong>Stress Periods:</strong> {len(stress_periods)} sustained high-load periods detected in selected range</li>
#         <li><strong>Backlog Status:</strong> {'Critical accumulation detected' if has_backlog else 'Within normal parameters'}</li>
#         <li><strong>Net Intake:</strong> {'Positive pressure - system accumulating' if net_intake > 0 else 'Negative - system relieving'}</li>
#         <li><strong>Forecast Trend:</strong> {'Increasing' if trend_change > 0 else 'Decreasing'} ({trend_change:+.1f}%)</li>
#     </ul>
# </div>
# """, unsafe_allow_html=True)

# if stress_level >= 5 or has_backlog or total_load > alert_threshold:
#     recommendation = "URGENT: Expand HHS capacity and accelerate discharge procedures. System showing sustained strain."
#     rec_color = "#EF4444"
# elif stress_level >= 3 or net_intake > 5:
#     recommendation = "WARNING: Monitor closely and prepare contingency plans. Moderate pressure detected."
#     rec_color = "#F59E0B"
# else:
#     recommendation = "System operating within sustainable limits. Maintain current operations and continue monitoring."
#     rec_color = "#10B981"

# st.markdown(f"""
# <div style="background: linear-gradient(135deg, rgba({','.join(['239', '68', '68'] if stress_level >= 5 or total_load > alert_threshold else ['245', '158', '11'] if stress_level >= 3 else ['16', '185', '129'])}, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
#             border-left: 4px solid {rec_color}; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
#     <h4 style="color: {rec_color}; margin-bottom: 0.5rem;">📋 Primary Recommendation</h4>
#     <p style="color: #E2E8F0; font-size: 1.05rem;">{recommendation}</p>
# </div>
# """, unsafe_allow_html=True)

# # ============================================================
# # SECTION 10: SUMMARY STATISTICS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">📊 Summary Statistics</div>', unsafe_allow_html=True)

# summary_df = pd.DataFrame({
#     "Metric": [
#         "Average Daily Intake (CBP)",
#         "Average CBP Custody Load",
#         "Average HHS Care Load",
#         "Average Daily Transfers",
#         "Average Daily Discharges",
#         "Average Total System Load",
#         "Peak System Load",
#         "Minimum System Load",
#         "Average Net Daily Intake",
#         "Average 14-Day Backlog"
#     ],
#     "Value": [
#         f"{filtered_df['apprehended'].mean():.0f}",
#         f"{filtered_df['in_cbp'].mean():.0f}",
#         f"{filtered_df['in_hhs'].mean():.0f}",
#         f"{filtered_df['transferred'].mean():.0f}",
#         f"{filtered_df['discharged'].mean():.0f}",
#         f"{filtered_df['Total_System_Load'].mean():.0f}",
#         f"{filtered_df['Total_System_Load'].max():.0f}",
#         f"{filtered_df['Total_System_Load'].min():.0f}",
#         f"{filtered_df['Net_Daily_Intake'].mean():+.1f}",
#         f"{filtered_df['Backlog_14d'].mean():.1f}"
#     ]
# })

# st.dataframe(summary_df, use_container_width=True, hide_index=True)

# # ============================================================
# # SECTION 11: PDF REPORT GENERATOR (NEW FEATURE)
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">📄 Generate Executive Report</div>', unsafe_allow_html=True)

# def generate_pdf_report():
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
#     styles = getSampleStyleSheet()
    
#     # Custom styles
#     title_style = ParagraphStyle(
#         'CustomTitle',
#         parent=styles['Heading1'],
#         fontSize=20,
#         textColor=colors.HexColor('#667eea'),
#         spaceAfter=20,
#         alignment=TA_CENTER,
#         fontName='Helvetica-Bold'
#     )
    
#     heading_style = ParagraphStyle(
#         'CustomHeading',
#         parent=styles['Heading2'],
#         fontSize=14,
#         textColor=colors.HexColor('#764ba2'),
#         spaceAfter=10,
#         spaceBefore=15,
#         fontName='Helvetica-Bold'
#     )
    
#     body_style = ParagraphStyle(
#         'CustomBody',
#         parent=styles['Normal'],
#         fontSize=10,
#         textColor=colors.HexColor('#333333'),
#         alignment=TA_JUSTIFY,
#         spaceAfter=8
#     )
    
#     story = []
    
#     # Title
#     story.append(Paragraph("UAC System Capacity & Care Load Analytics", title_style))
#     story.append(Paragraph(f"Executive Report - Generated: {datetime.now().strftime('%B %d, %Y')}", body_style))
#     story.append(Spacer(1, 20))
    
#     # Executive Summary
#     story.append(Paragraph("Executive Summary", heading_style))
#     story.append(Paragraph(f"""
#     This report analyzes the capacity and care load of the Unaccompanied Children (UAC) Program 
#     from {start_date} to {end_date}. The system currently cares for <b>{total_load:,} children</b> 
#     with a stress level classified as <b>{stress_status}</b>.
#     """, body_style))
#     story.append(Spacer(1, 10))
    
#     # Key Metrics Table
#     story.append(Paragraph("Key Performance Indicators", heading_style))
#     kpi_data = [
#         ["Metric", "Value", "Status"],
#         ["Total Children Under Care", f"{total_load:,}", stress_status],
#         ["Daily Intake (Transfers)", f"{daily_intake:,}", "Active"],
#         ["Daily Outflow (Discharges)", f"{daily_outflow:,}", "Active"],
#         ["Net Intake Pressure", f"{net_intake:+.0f}", pressure_text],
#         ["14-Day Backlog", f"{backlog_trend:+.0f}", backlog_status]
#     ]
    
#     kpi_table = Table(kpi_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
#     kpi_table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 11),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
#         ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
#         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 1), (-1, -1), 9),
#         ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white])
#     ]))
#     story.append(kpi_table)
#     story.append(Spacer(1, 15))
    
#     # Findings
#     story.append(Paragraph("Key Findings", heading_style))
#     findings = f"""
#     <ul>
#         <li>System Load: Currently <b>{total_load:,} children</b> under care</li>
#         <li>Stress Periods: {len(stress_periods)} sustained high-load periods detected</li>
#         <li>Backlog Status: {'Critical accumulation detected' if has_backlog else 'Within normal parameters'}</li>
#         <li>Net Intake: {'Positive pressure - system accumulating' if net_intake > 0 else 'Negative - system relieving'}</li>
#         <li>Forecast Trend: {'Increasing' if trend_change > 0 else 'Decreasing'} ({trend_change:+.1f}%)</li>
#     </ul>
#     """
#     story.append(Paragraph(findings, body_style))
#     story.append(Spacer(1, 10))
    
#     # Recommendation
#     story.append(Paragraph("Primary Recommendation", heading_style))
#     story.append(Paragraph(f"<b>Status:</b> {rec_color.replace('#', '')}<br/>{recommendation}", body_style))
#     story.append(Spacer(1, 10))
    
#     # Summary Statistics
#     story.append(Paragraph("Summary Statistics", heading_style))
#     stats_data = [["Metric", "Value"]] + [[row["Metric"], row["Value"]] for _, row in summary_df.iterrows()]
#     stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
#     stats_table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 10),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
#         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 1), (-1, -1), 9),
#         ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white])
#     ]))
#     story.append(stats_table)
    
#     # Footer
#     story.append(Spacer(1, 30))
#     story.append(Paragraph("""
#     <hr/>
#     <p align="center" style="font-size: 8pt; color: #666;">
#     UAC System Capacity & Care Load Analytics | Unified Mentor Project<br/>
#     Data Source: U.S. Department of Health and Human Services | UAC Program<br/>
#     Generated automatically from Streamlit Dashboard
#     </p>
#     """, body_style))
    
#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# if st.button("📄 Generate PDF Report"):
#     with st.spinner("Generating executive report..."):
#         pdf_buffer = generate_pdf_report()
#         st.download_button(
#             label="⬇️ Download PDF Report",
#             data=pdf_buffer,
#             file_name=f"UAC_Capacity_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
#             mime="application/pdf"
#         )
#         st.success("✅ Report generated successfully!")

# # ============================================================
# # SECTION 12: DOWNLOADS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">💾 Export Data</div>', unsafe_allow_html=True)

# dl_col1, dl_col2, dl_col3 = st.columns(3)

# with dl_col1:
#     forecast_csv = pd.DataFrame({
#         "Date": forecast["ds"],
#         "Forecast": forecast["yhat"],
#         "Lower_Bound": forecast["yhat_lower"],
#         "Upper_Bound": forecast["yhat_upper"]
#     }).to_csv(index=False)
#     st.download_button("⬇️ Download Forecast CSV", forecast_csv, 
#                        f"capacity_forecast_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# with dl_col2:
#     full_csv = filtered_df[["date", "in_cbp", "in_hhs", "transferred", "discharged", 
#                            "Total_System_Load", "Net_Daily_Intake", "Backlog_14d"]].to_csv(index=False)
#     st.download_button("📊 Download Full Data CSV", full_csv,
#                        f"uac_capacity_data_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# with dl_col3:
#     kpi_csv = pd.DataFrame({
#         "KPI": ["Total Children", "Net Intake Pressure", "Load Volatility", "Backlog Rate", "Discharge Ratio"],
#         "Value": [f"{latest['KPI_Total_Load']:.0f}", f"{latest['KPI_Net_Intake']:.2f}",
#                   f"{latest['KPI_Volatility']:.2f}%", f"{latest['KPI_Backlog_Rate']:.2f}", f"{latest['KPI_Discharge_Ratio']:.2f}"],
#         "Status": ["Good" if latest['KPI_Total_Load'] < alert_threshold else "Warning" if latest['KPI_Total_Load'] < alert_threshold * 1.25 else "Critical",
#                    "Good" if latest['KPI_Net_Intake'] < 0 else "Warning" if latest['KPI_Net_Intake'] < 10 else "Critical",
#                    "Stable" if latest['KPI_Volatility'] < 5 else "Moderate" if latest['KPI_Volatility'] < 10 else "High",
#                    "Good" if latest['KPI_Backlog_Rate'] < 0 else "Warning" if latest['KPI_Backlog_Rate'] < 5 else "Critical",
#                    "Balanced" if 0.8 <= latest['KPI_Discharge_Ratio'] <= 1.2 else "Imbalanced"]
#     }).to_csv(index=False)
#     st.download_button("📈 Download KPI Summary", kpi_csv,
#                        f"kpi_summary_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# # ============================================================
# # FOOTER
# # ============================================================
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; color: #64748B; padding: 1.5rem; border-top: 1px solid rgba(102, 126, 234, 0.2);">
#     <p style="font-size: 1.1rem; font-weight: 600; color: #94A3B8;">
#         🏥 UAC System Capacity & Care Load Analytics
#     </p>
#     <p>Unified Mentor Project | Built with Streamlit, Prophet & Plotly</p>
#     <p style="font-size: 0.8rem; color: #475569;">
#         Data Source: U.S. Department of Health and Human Services | UAC Program
#     </p>
# </div>
# """, unsafe_allow_html=True)








#code-1

# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from prophet import Prophet
# from datetime import datetime, timedelta
# import warnings
# import os

# warnings.filterwarnings('ignore')

# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================
# st.set_page_config(
#     page_title="UAC System Capacity & Care Load Analytics",
#     page_icon="🏥",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS - Professional Dark Theme
# st.markdown("""
# <style>
#     .main-header { 
#         font-size: 2.8rem; 
#         font-weight: 800; 
#         color: #E2E8F0; 
#         text-align: center;
#         margin-bottom: 0.3rem;
#         letter-spacing: -0.5px;
#     }
#     .sub-header { 
#         font-size: 1.15rem; 
#         color: #94A3B8; 
#         text-align: center;
#         margin-bottom: 2.5rem;
#         font-weight: 400;
#     }
#     .kpi-card {
#         background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
#         backdrop-filter: blur(10px);
#         border: 1px solid rgba(102, 126, 234, 0.3);
#         padding: 1.8rem 1.2rem;
#         border-radius: 16px;
#         color: #E2E8F0;
#         text-align: center;
#         box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
#         transition: transform 0.3s ease;
#     }
#     .kpi-card:hover {
#         transform: translateY(-5px);
#         border-color: rgba(102, 126, 234, 0.6);
#     }
#     .kpi-value { 
#         font-size: 2.6rem; 
#         font-weight: 800;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.3rem;
#     }
#     .kpi-label { 
#         font-size: 0.85rem; 
#         color: #94A3B8;
#         text-transform: uppercase;
#         letter-spacing: 1px;
#         margin-bottom: 0.5rem;
#     }
#     .kpi-status {
#         font-size: 0.8rem;
#         padding: 0.3rem 0.8rem;
#         border-radius: 20px;
#         display: inline-block;
#         font-weight: 600;
#     }
#     .status-good { background: rgba(16, 185, 129, 0.2); color: #10B981; }
#     .status-warning { background: rgba(245, 158, 11, 0.2); color: #F59E0B; }
#     .status-danger { background: rgba(239, 68, 68, 0.2); color: #EF4444; }
#     .section-title {
#         font-size: 1.5rem;
#         font-weight: 700;
#         color: #E2E8F0;
#         margin-top: 2.5rem;
#         margin-bottom: 1.2rem;
#         padding-left: 1.2rem;
#         border-left: 4px solid #667eea;
#     }
#     .section-subtitle {
#         font-size: 0.95rem;
#         color: #64748B;
#         margin-bottom: 1.5rem;
#         padding-left: 1.2rem;
#     }
#     .alert-box { 
#         padding: 1.2rem; 
#         border-radius: 12px; 
#         margin: 1rem 0; 
#         border-left: 4px solid;
#         background: rgba(15, 23, 42, 0.8);
#     }
#     .alert-danger { border-color: #EF4444; }
#     .alert-warning { border-color: #F59E0B; }
#     .alert-success { border-color: #10B981; }
#     .alert-info { border-color: #3B82F6; }
#     .insight-card {
#         background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
#         border: 1px solid rgba(16, 185, 129, 0.2);
#         padding: 1.5rem;
#         border-radius: 12px;
#         margin: 1rem 0;
#     }
#     .stress-meter {
#         height: 8px;
#         border-radius: 4px;
#         background: linear-gradient(90deg, #10B981 0%, #F59E0B 50%, #EF4444 100%);
#         position: relative;
#     }
#     .stress-marker {
#         width: 4px;
#         height: 16px;
#         background: white;
#         position: absolute;
#         top: -4px;
#         border-radius: 2px;
#         box-shadow: 0 0 10px rgba(255,255,255,0.5);
#     }
# </style>
# """, unsafe_allow_html=True)

# # ============================================================
# # HEADER
# # ============================================================
# st.markdown('<div class="main-header">🏥 System Capacity & Care Load Analytics</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-header">Unaccompanied Children (UAC) Program | Real-Time Capacity Monitoring & Stress Detection</div>', unsafe_allow_html=True)

# # ============================================================
# # LOAD DATA
# # ============================================================
# @st.cache_data(ttl=3600)
# def load_data():
#     possible_paths = [
#         "data/HHS_Unaccompanied_Alien_Children_Program.csv",
#         "../data/HHS_Unaccompanied_Alien_Children_Program.csv",
#         "HHS_Unaccompanied_Alien_Children_Program.csv",
#         "data/uac_capacity_data.csv",
#         "../data/uac_capacity_data.csv"
#     ]
    
#     df = None
#     used_path = None
    
#     for path in possible_paths:
#         if os.path.exists(path):
#             try:
#                 df = pd.read_csv(path)
#                 used_path = path
#                 break
#             except Exception:
#                 continue
    
#     if df is not None:
#         st.success(f"✅ Data loaded from: {used_path}")
        
#         # DEBUG: Show original columns
#         st.info(f"📋 Original columns: {list(df.columns)}")
        
#         # FIXED: More precise column mapping - check more specific names FIRST
#         col_mapping = {}
#         for col in df.columns:
#             col_lower = col.lower().strip()
#             # Date column
#             if 'date' in col_lower:
#                 col_mapping[col] = 'date'
#             # Transferred out of CBP - MUST check BEFORE 'in cbp'
#             elif 'transferred out' in col_lower or 'transferred_out' in col_lower:
#                 col_mapping[col] = 'transferred'
#             # Discharged from HHS - MUST check BEFORE 'in hhs'
#             elif 'discharged' in col_lower or 'discharge' in col_lower:
#                 col_mapping[col] = 'discharged'
#             # Apprehended / Intake column
#             elif 'apprehended' in col_lower or 'placed in cbp' in col_lower or 'placed_in_cbp' in col_lower:
#                 col_mapping[col] = 'apprehended'
#             # Children in CBP custody - check AFTER transferred
#             elif 'in cbp' in col_lower or 'in_cbp' in col_lower or 'cbp custody' in col_lower:
#                 col_mapping[col] = 'in_cbp'
#             # Children in HHS care - check AFTER discharged
#             elif 'in hhs' in col_lower or 'in_hhs' in col_lower or 'hhs care' in col_lower:
#                 col_mapping[col] = 'in_hhs'
        
#         st.info(f"🔄 Column mapping: {col_mapping}")
        
#         df = df.rename(columns=col_mapping)
#         df["date"] = pd.to_datetime(df["date"])
        
#         # Remove duplicate columns if any
#         if df.columns.duplicated().any():
#             df = df.loc[:, ~df.columns.duplicated()]
        
#         # Convert numeric columns safely
#         for col in ["apprehended", "in_cbp", "transferred", "in_hhs", "discharged"]:
#             if col in df.columns:
#                 df[col] = df[col].apply(
#                     lambda x: pd.to_numeric(str(x).replace(',', '').replace('$', '').strip(), errors='coerce')
#                 )
        
#         # Check which required columns are available
#         required_cols = ["date", "apprehended", "in_cbp", "transferred", "in_hhs", "discharged"]
#         available_cols = [c for c in required_cols if c in df.columns]
#         missing_cols = [c for c in required_cols if c not in df.columns]
        
#         if missing_cols:
#             st.warning(f"⚠️ Missing columns: {missing_cols}")
        
#         df = df[available_cols].dropna().sort_values("date").reset_index(drop=True)
#         return df
    
#     # Generate realistic synthetic data
#     st.info("📊 Using synthetic data for demonstration...")
#     dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq="D")
#     np.random.seed(42)
#     n_days = len(dates)
    
#     day_of_year = dates.dayofyear
#     seasonal = 1 + 0.35 * np.sin(2 * np.pi * (day_of_year - 60) / 365)
#     policy_effect = np.ones(n_days)
#     policy_effect[400:450] = 0.6
#     policy_effect[700:750] = 1.4
    
#     trend = np.linspace(1.0, 1.2, n_days)
    
#     base_intake = (120 * seasonal * trend * policy_effect + np.random.normal(0, 20, n_days)).astype(int)
#     base_intake = np.maximum(base_intake, 15)
    
#     cbp = np.zeros(n_days)
#     cbp[0] = base_intake[0]
#     for i in range(1, n_days):
#         outflow = int(cbp[i-1] * np.random.uniform(0.2, 0.4))
#         cbp[i] = max(0, min(2500, cbp[i-1] + base_intake[i] - outflow))
    
#     transfers = np.minimum(
#         (cbp * np.random.uniform(0.5, 0.85, n_days) + np.random.normal(0, 8, n_days)).astype(int),
#         cbp
#     )
#     transfers = np.maximum(transfers, 0)
    
#     hhs = np.zeros(n_days)
#     hhs[0] = transfers[0]
#     for i in range(1, n_days):
#         discharge_rate = np.random.uniform(0.06, 0.2)
#         discharges_today = int(hhs[i-1] * discharge_rate)
#         hhs[i] = max(0, hhs[i-1] + transfers[i] - discharges_today)
    
#     discharges = np.zeros(n_days)
#     for i in range(1, n_days):
#         discharge_rate = np.random.uniform(0.06, 0.2)
#         discharges[i] = int(hhs[i-1] * discharge_rate)
#     discharges = np.minimum(discharges, hhs)
    
#     df = pd.DataFrame({
#         "date": dates,
#         "apprehended": base_intake.astype(int),
#         "in_cbp": cbp.astype(int),
#         "transferred": transfers.astype(int),
#         "in_hhs": hhs.astype(int),
#         "discharged": discharges.astype(int)
#     })
#     return df

# df = load_data()

# # ============================================================
# # BACKEND LOGIC - DERIVED HEALTHCARE CAPACITY METRICS
# # ============================================================

# df["Total_System_Load"] = df["in_cbp"] + df["in_hhs"]
# df["Net_Daily_Intake"] = df["transferred"] - df["discharged"]
# df["Growth_Rate"] = df["Total_System_Load"].pct_change() * 100

# df["Load_Rolling_7d"] = df["Total_System_Load"].rolling(window=7, min_periods=1).mean()
# df["Load_Rolling_14d"] = df["Total_System_Load"].rolling(window=14, min_periods=1).mean()
# df["CBP_Rolling_7d"] = df["in_cbp"].rolling(window=7, min_periods=1).mean()
# df["CBP_Rolling_14d"] = df["in_cbp"].rolling(window=14, min_periods=1).mean()
# df["HHS_Rolling_7d"] = df["in_hhs"].rolling(window=7, min_periods=1).mean()
# df["HHS_Rolling_14d"] = df["in_hhs"].rolling(window=14, min_periods=1).mean()

# df["Backlog_7d"] = df["Net_Daily_Intake"].rolling(window=7, min_periods=1).sum()
# df["Backlog_14d"] = df["Net_Daily_Intake"].rolling(window=14, min_periods=1).sum()

# df["Load_Volatility"] = df["Total_System_Load"].rolling(window=14, min_periods=1).std()
# df["CBP_Volatility"] = df["in_cbp"].rolling(window=7, min_periods=1).std()
# df["HHS_Volatility"] = df["in_hhs"].rolling(window=7, min_periods=1).std()

# df["Stress_Flag"] = df["Total_System_Load"] > df["Load_Rolling_14d"] * 1.1
# df["Sustained_Stress"] = df["Stress_Flag"].rolling(window=7, min_periods=1).sum()

# df["KPI_Total_Load"] = df["Total_System_Load"]
# df["KPI_Net_Intake"] = df["Net_Daily_Intake"].rolling(window=7, min_periods=1).mean()
# df["KPI_Volatility"] = (df["Load_Volatility"] / df["Total_System_Load"].rolling(window=14, min_periods=1).mean()) * 100
# df["KPI_Backlog_Rate"] = df["Backlog_14d"] / 14
# df["KPI_Discharge_Ratio"] = df["discharged"] / df["transferred"].replace(0, np.nan)

# df = df.fillna(0)

# # ============================================================
# # SIDEBAR - CONTROL PANEL
# # ============================================================
# st.sidebar.markdown("## ⚙️ Control Panel")
# st.sidebar.markdown("---")

# min_date = df["date"].min().date()
# max_date = df["date"].max().date()

# col1, col2 = st.sidebar.columns(2)
# with col1:
#     start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
# with col2:
#     end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# mask = (df["date"] >= pd.Timestamp(start_date)) & (df["date"] <= pd.Timestamp(end_date))
# filtered_df = df[mask].copy()

# st.sidebar.markdown("---")

# granularity = st.sidebar.selectbox("⏱️ Time Granularity", ["Daily", "Weekly", "Monthly"], index=0)

# if granularity == "Weekly":
#     filtered_df = filtered_df.set_index("date").resample("W").mean().reset_index()
#     filtered_df["date"] = filtered_df["date"].dt.to_period("W").dt.start_time
# elif granularity == "Monthly":
#     filtered_df = filtered_df.set_index("date").resample("M").mean().reset_index()
#     filtered_df["date"] = filtered_df["date"].dt.to_period("M").dt.start_time

# st.sidebar.markdown("---")
# st.sidebar.markdown("### 📊 Display Options")
# show_cbp = st.sidebar.checkbox("Show CBP Load", value=True)
# show_hhs = st.sidebar.checkbox("Show HHS Load", value=True)
# show_total = st.sidebar.checkbox("Show Total System Load", value=True)
# show_rolling = st.sidebar.checkbox("Show Rolling Averages", value=True)
# show_stress = st.sidebar.checkbox("Highlight Stress Periods", value=True)

# st.sidebar.markdown("---")
# st.sidebar.markdown("### 🔮 Forecast")
# forecast_days = st.sidebar.slider("Forecast Days", 30, 365, 90)

# # ============================================================
# # LATEST DATA FOR KPIs
# # ============================================================
# latest = filtered_df.iloc[-1] if len(filtered_df) > 0 else df.iloc[-1]

# stress_level = latest["Sustained_Stress"]
# if stress_level >= 5:
#     stress_status = "CRITICAL"
#     stress_class = "status-danger"
# elif stress_level >= 3:
#     stress_status = "ELEVATED"
#     stress_class = "status-warning"
# else:
#     stress_status = "NORMAL"
#     stress_class = "status-good"

# backlog_trend = latest["Backlog_14d"]
# if backlog_trend > 50:
#     backlog_status = "ACCUMULATING"
#     backlog_class = "status-danger"
# elif backlog_trend > 0:
#     backlog_status = "GROWING"
#     backlog_class = "status-warning"
# else:
#     backlog_status = "STABLE"
#     backlog_class = "status-good"

# # ============================================================
# # SECTION 1: KPI SUMMARY CARDS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">📊 System Capacity Overview</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">Real-time monitoring of total care load, intake pressure, and system stress levels</div>', unsafe_allow_html=True)

# kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

# with kpi_col1:
#     total_load = int(latest["KPI_Total_Load"])
#     st.markdown(f"""
#     <div class="kpi-card">
#         <div class="kpi-value">{total_load:,}</div>
#         <div class="kpi-label">Total Children Under Care</div>
#         <div class="kpi-status {stress_class}">{stress_status}</div>
#     </div>
#     """, unsafe_allow_html=True)

# with kpi_col2:
#     daily_intake = int(latest["transferred"])
#     st.markdown(f"""
#     <div class="kpi-card">
#         <div class="kpi-value">{daily_intake:,}</div>
#         <div class="kpi-label">Daily Intake (Transfers)</div>
#         <div class="kpi-status status-info">Into HHS System</div>
#     </div>
#     """, unsafe_allow_html=True)

# with kpi_col3:
#     daily_outflow = int(latest["discharged"])
#     st.markdown(f"""
#     <div class="kpi-card">
#         <div class="kpi-value">{daily_outflow:,}</div>
#         <div class="kpi-label">Daily Outflow (Discharges)</div>
#         <div class="kpi-status status-info">To Sponsors</div>
#     </div>
#     """, unsafe_allow_html=True)

# with kpi_col4:
#     net_intake = latest["KPI_Net_Intake"]
#     pressure_color = "status-danger" if net_intake > 10 else "status-warning" if net_intake > 0 else "status-good"
#     pressure_text = "HIGH PRESSURE" if net_intake > 10 else "MODERATE" if net_intake > 0 else "BALANCED"
#     st.markdown(f"""
#     <div class="kpi-card">
#         <div class="kpi-value">{net_intake:+.0f}</div>
#         <div class="kpi-label">Net Intake Pressure</div>
#         <div class="kpi-status {pressure_color}">{pressure_text}</div>
#     </div>
#     """, unsafe_allow_html=True)

# # ============================================================
# # STRESS METER
# # ============================================================
# st.markdown("---")
# stress_col1, stress_col2 = st.columns([3, 1])

# with stress_col1:
#     st.markdown('<div class="section-title">🔥 System Stress Indicator</div>', unsafe_allow_html=True)
#     current_stress = min(stress_level / 7 * 100, 100)
#     st.markdown(f"""
#     <div style="background: rgba(15, 23, 42, 0.8); padding: 1.5rem; border-radius: 12px;">
#         <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
#             <span style="color: #10B981; font-weight: 600;">Normal</span>
#             <span style="color: #F59E0B; font-weight: 600;">Elevated</span>
#             <span style="color: #EF4444; font-weight: 600;">Critical</span>
#         </div>
#         <div class="stress-meter">
#             <div class="stress-marker" style="left: {current_stress}%;"></div>
#         </div>
#         <div style="text-align: center; margin-top: 1rem; color: #94A3B8;">
#             Current Stress Level: <strong style="color: {'#EF4444' if stress_level >= 5 else '#F59E0B' if stress_level >= 3 else '#10B981'};">{stress_level}/7 days</strong> sustained pressure
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# with stress_col2:
#     st.markdown('<div class="section-title">📈 Backlog Trend</div>', unsafe_allow_html=True)
#     st.markdown(f"""
#     <div style="background: rgba(15, 23, 42, 0.8); padding: 1.5rem; border-radius: 12px; text-align: center;">
#         <div style="font-size: 2.2rem; font-weight: 800; color: {'#EF4444' if backlog_trend > 50 else '#F59E0B' if backlog_trend > 0 else '#10B981'};">{backlog_trend:+.0f}</div>
#         <div style="color: #94A3B8; font-size: 0.9rem;">14-Day Accumulation</div>
#         <div class="kpi-status {backlog_class}" style="margin-top: 0.8rem;">{backlog_status}</div>
#     </div>
#     """, unsafe_allow_html=True)

# # ============================================================
# # SECTION 2: TIME SERIES ANALYSIS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">📈 Time Series Analysis: System Load & Pressure Detection</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">When the daily load (solid line) rises above the 14-day rolling average (dashed), the system enters a stress period</div>', unsafe_allow_html=True)

# fig_load = go.Figure()

# if show_total:
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["Total_System_Load"],
#         mode="lines", name="Total System Load",
#         line=dict(color="#667eea", width=2),
#         fill="tozeroy", fillcolor="rgba(102, 126, 234, 0.08)",
#         hovertemplate="<b>Total Load</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>"
#     ))

# if show_cbp:
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["in_cbp"],
#         mode="lines", name="CBP Custody",
#         line=dict(color="#f5576c", width=1.5),
#         hovertemplate="<b>CBP</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>"
#     ))

# if show_hhs:
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["in_hhs"],
#         mode="lines", name="HHS Care",
#         line=dict(color="#11998e", width=1.5),
#         hovertemplate="<b>HHS</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>"
#     ))

# if show_rolling:
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["Load_Rolling_7d"],
#         mode="lines", name="7-Day Rolling Avg",
#         line=dict(color="#F59E0B", width=2, dash="dash"),
#         hovertemplate="<b>7-Day Avg</b><br>Date: %{x}<br>Avg: %{y:,.0f}<extra></extra>"
#     ))
#     fig_load.add_trace(go.Scatter(
#         x=filtered_df["date"], y=filtered_df["Load_Rolling_14d"],
#         mode="lines", name="14-Day Rolling Avg",
#         line=dict(color="#EF4444", width=2, dash="dot"),
#         hovertemplate="<b>14-Day Avg</b><br>Date: %{x}<br>Avg: %{y:,.0f}<extra></extra>"
#     ))

# if show_stress:
#     stress_df = filtered_df[filtered_df["Stress_Flag"] == True]
#     if len(stress_df) > 0:
#         fig_load.add_trace(go.Scatter(
#             x=stress_df["date"], y=stress_df["Total_System_Load"],
#             mode="markers", name="⚠️ Stress Period",
#             marker=dict(color="#EF4444", size=8, symbol="diamond"),
#             hovertemplate="<b>STRESS ALERT</b><br>Date: %{x}<br>Load: %{y:,.0f}<extra></extra>"
#         ))

# fig_load.update_layout(
#     height=500,
#     template="plotly_dark",
#     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#     yaxis_title="Number of Children",
#     xaxis_title="Date",
#     hovermode="x unified"
# )

# st.plotly_chart(fig_load, use_container_width=True)

# # ============================================================
# # SECTION 3: SYSTEM BALANCE
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">⚖️ System Balance: Intake vs Discharge Gap</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">Persistent positive gap indicates backlog accumulation and capacity strain</div>', unsafe_allow_html=True)

# fig_balance = make_subplots(
#     rows=2, cols=1,
#     subplot_titles=("Net Daily Intake (Transfers - Discharges)", "14-Day Backlog Accumulation Trend"),
#     vertical_spacing=0.15
# )

# colors = ["#10B981" if x < 0 else "#EF4444" if x > 10 else "#F59E0B" for x in filtered_df["Net_Daily_Intake"]]
# fig_balance.add_trace(go.Bar(
#     x=filtered_df["date"], y=filtered_df["Net_Daily_Intake"],
#     name="Net Intake", marker_color=colors, opacity=0.8,
#     hovertemplate="<b>Net Intake</b><br>Date: %{x}<br>Value: %{y:+.0f}<extra></extra>"
# ), row=1, col=1)

# fig_balance.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
# fig_balance.add_hline(y=10, line_dash="dot", line_color="#EF4444", row=1, col=1,
#                        annotation_text="Critical Threshold", annotation_position="top right")

# fig_balance.add_trace(go.Scatter(
#     x=filtered_df["date"], y=filtered_df["Backlog_14d"],
#     mode="lines", name="14-Day Backlog", fill="tozeroy",
#     line=dict(color="#667eea", width=2),
#     fillcolor="rgba(102, 126, 234, 0.15)",
#     hovertemplate="<b>14-Day Backlog</b><br>Date: %{x}<br>Accumulation: %{y:+.0f}<extra></extra>"
# ), row=2, col=1)

# fig_balance.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)

# fig_balance.update_layout(
#     height=650,
#     template="plotly_dark",
#     showlegend=True,
#     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
# )

# st.plotly_chart(fig_balance, use_container_width=True)

# # ============================================================
# # SECTION 4: PRESSURE & STRESS IDENTIFICATION
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">🔍 Pressure & Stress Identification</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">Rolling averages and variability analysis to detect prolonged strain windows</div>', unsafe_allow_html=True)

# fig_stress = make_subplots(
#     rows=2, cols=2,
#     subplot_titles=(
#         "CBP: 7-Day vs 14-Day Rolling Average",
#         "HHS: 7-Day vs 14-Day Rolling Average",
#         "CBP Load Variability (7d Std Dev)",
#         "HHS Load Variability (7d Std Dev)"
#     ),
#     vertical_spacing=0.12, horizontal_spacing=0.08
# )

# fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["CBP_Rolling_7d"], 
#                mode="lines", name="CBP 7d", line=dict(color="#f5576c")), row=1, col=1)
# fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["CBP_Rolling_14d"], 
#                mode="lines", name="CBP 14d", line=dict(color="#f093fb", dash="dash")), row=1, col=1)

# fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["HHS_Rolling_7d"], 
#                mode="lines", name="HHS 7d", line=dict(color="#11998e")), row=1, col=2)
# fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["HHS_Rolling_14d"], 
#                mode="lines", name="HHS 14d", line=dict(color="#38ef7d", dash="dash")), row=1, col=2)

# fig_stress.add_trace(go.Bar(x=filtered_df["date"], y=filtered_df["CBP_Volatility"], 
#            marker_color="#f5576c", opacity=0.6, name="CBP Volatility"), row=2, col=1)
# fig_stress.add_trace(go.Bar(x=filtered_df["date"], y=filtered_df["HHS_Volatility"], 
#            marker_color="#11998e", opacity=0.6, name="HHS Volatility"), row=2, col=2)

# fig_stress.update_layout(height=650, template="plotly_dark", showlegend=False)
# st.plotly_chart(fig_stress, use_container_width=True)

# # ============================================================
# # SECTION 5: CAPACITY DISTRIBUTION & FLOW
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">🏛️ Capacity Distribution & Flow Analysis</div>', unsafe_allow_html=True)

# fig_dist = make_subplots(
#     rows=1, cols=2,
#     specs=[[{"type": "pie"}, {"type": "xy"}]],
#     subplot_titles=("Current Load Distribution", "Transfer vs Discharge Flow")
# )

# latest_data = filtered_df.iloc[-1] if len(filtered_df) > 0 else df.iloc[-1]

# fig_dist.add_trace(go.Pie(
#     labels=["CBP Custody", "HHS Care"],
#     values=[latest_data["in_cbp"], latest_data["in_hhs"]],
#     hole=0.55,
#     marker_colors=["#f5576c", "#11998e"],
#     textinfo="label+percent",
#     textfont=dict(size=12, color="white")
# ), row=1, col=1)

# fig_dist.add_trace(go.Scatter(
#     x=filtered_df["date"], y=filtered_df["transferred"],
#     mode="lines", name="Transfers to HHS", line=dict(color="#667eea", width=2),
#     fill="tozeroy", fillcolor="rgba(102, 126, 234, 0.15)"
# ), row=1, col=2)

# fig_dist.add_trace(go.Scatter(
#     x=filtered_df["date"], y=filtered_df["discharged"],
#     mode="lines", name="Discharges from HHS", line=dict(color="#10B981", width=2),
#     fill="tozeroy", fillcolor="rgba(16, 185, 129, 0.15)"
# ), row=1, col=2)

# fig_dist.update_layout(height=400, template="plotly_dark", showlegend=True,
#                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
# st.plotly_chart(fig_dist, use_container_width=True)

# # ============================================================
# # SECTION 6: AI FORECASTING
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">🔮 AI Forecasting: Total System Load Prediction</div>', unsafe_allow_html=True)
# st.markdown('<div class="section-subtitle">Prophet model predicts capacity needs for the next {} days with confidence intervals</div>'.format(forecast_days), unsafe_allow_html=True)

# prophet_df = filtered_df[["date", "Total_System_Load"]].rename(columns={"date": "ds", "Total_System_Load": "y"})

# model = Prophet(
#     yearly_seasonality=True,
#     weekly_seasonality=True,
#     daily_seasonality=False,
#     changepoint_prior_scale=0.05,
#     seasonality_prior_scale=10.0,
#     growth="flat"
# )

# if len(prophet_df) > 365:
#     model.add_seasonality(name="monthly", period=30.5, fourier_order=5)

# model.fit(prophet_df)

# future = model.make_future_dataframe(periods=forecast_days)
# future["floor"] = prophet_df["y"].min() * 0.5

# forecast = model.predict(future)

# min_forecast = max(prophet_df["y"].min() * 0.3, 100)
# forecast["yhat"] = np.maximum(forecast["yhat"], min_forecast)
# forecast["yhat_lower"] = np.maximum(forecast["yhat_lower"], min_forecast * 0.5)
# forecast["yhat_upper"] = np.maximum(forecast["yhat_upper"], min_forecast)

# fig_forecast = go.Figure()
# fig_forecast.add_trace(go.Scatter(
#     x=prophet_df["ds"], y=prophet_df["y"],
#     name="Actual Load", mode="lines", line=dict(color="#3B82F6", width=2)
# ))
# fig_forecast.add_trace(go.Scatter(
#     x=forecast["ds"], y=forecast["yhat"],
#     name="AI Forecast", mode="lines", line=dict(color="#10B981", width=2)
# ))
# fig_forecast.add_trace(go.Scatter(
#     x=forecast["ds"].tolist() + forecast["ds"].tolist()[::-1],
#     y=forecast["yhat_upper"].tolist() + forecast["yhat_lower"].tolist()[::-1],
#     fill="toself", fillcolor="rgba(16, 185, 129, 0.15)",
#     line=dict(color="rgba(255,255,255,0)"), name="Confidence Interval"
# ))

# fig_forecast.add_hline(y=1500, line_dash="dash", line_color="#EF4444",
#                         annotation_text="Capacity Alert (1,500)", annotation_position="top right")

# fig_forecast.update_layout(
#     title=f"Forecast for Total System Load ({forecast_days} days)",
#     yaxis_title="Total Children Under Care",
#     height=500, template="plotly_dark", hovermode="x unified"
# )
# st.plotly_chart(fig_forecast, use_container_width=True)

# future_value = forecast["yhat"].iloc[-1]
# recent_value = forecast["yhat"].iloc[-forecast_days] if len(forecast) > forecast_days else forecast["yhat"].iloc[len(forecast)//2]
# trend_change = ((future_value - recent_value) / recent_value * 100) if recent_value > 0 else 0

# insight_col1, insight_col2, insight_col3 = st.columns(3)
# with insight_col1:
#     if trend_change > 10:
#         st.error(f"🚨 Capacity Crisis\n+{trend_change:.1f}% predicted")
#     elif trend_change > 0:
#         st.warning(f"⚠️ Growing Load\n+{trend_change:.1f}% predicted")
#     else:
#         st.success(f"✅ Capacity Relief\n{trend_change:.1f}% predicted")

# with insight_col2:
#     peak_date = forecast.loc[forecast["yhat"].idxmax(), "ds"]
#     st.info(f"📅 Predicted Peak\n{peak_date.strftime('%B %Y')}")

# with insight_col3:
#     conf_width = (forecast["yhat_upper"].iloc[-1] - forecast["yhat_lower"].iloc[-1]) / forecast["yhat"].iloc[-1] * 100
#     st.success(f"✅ Confidence\n±{conf_width/2:.1f}% uncertainty")

# # ============================================================
# # SECTION 7: DATA QUALITY & ANOMALIES
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">🔍 Data Quality & Logical Constraint Validation</div>', unsafe_allow_html=True)

# violations = []
# for idx, row in filtered_df.iterrows():
#     if row["transferred"] > row["in_cbp"]:
#         violations.append({"Date": row["date"], "Type": "Transfer > CBP Custody", "Severity": "Critical"})
#     if row["discharged"] > row["in_hhs"]:
#         violations.append({"Date": row["date"], "Type": "Discharge > HHS Care", "Severity": "Critical"})

# if violations:
#     st.warning(f"⚠️ {len(violations)} logical constraint violations detected")
#     st.dataframe(pd.DataFrame(violations), use_container_width=True)
# else:
#     st.success("✅ All logical constraints validated successfully (Transfers ≤ CBP, Discharges ≤ HHS)")

# # ============================================================
# # SECTION 8: EXECUTIVE INSIGHTS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">💡 Executive Insights & Recommendations</div>', unsafe_allow_html=True)

# stress_periods = []
# in_stress = False
# start_date_stress = None
# for idx, row in filtered_df.iterrows():
#     if row["Stress_Flag"] and not in_stress:
#         in_stress = True
#         start_date_stress = row["date"]
#     elif not row["Stress_Flag"] and in_stress:
#         in_stress = False
#         if start_date_stress:
#             duration = (row["date"] - start_date_stress).days if hasattr(row["date"], 'days') else 1
#             if duration >= 7:
#                 stress_periods.append(f"{start_date_stress.strftime('%Y-%m-%d')} to {row['date'].strftime('%Y-%m-%d')} ({duration} days)")

# sustained_backlog = filtered_df[filtered_df["Backlog_14d"] > 50]
# has_backlog = len(sustained_backlog) > 14

# st.markdown(f"""
# <div class="insight-card">
#     <h4 style="color: #E2E8F0; margin-bottom: 1rem;">🎯 Key Findings</h4>
#     <ul style="color: #CBD5E1; line-height: 2;">
#         <li><strong>System Load:</strong> Currently <span style="color: {'#EF4444' if total_load > 1500 else '#10B981'};">{total_load:,} children</span> under care</li>
#         <li><strong>Stress Periods:</strong> {len(stress_periods)} sustained high-load periods detected in selected range</li>
#         <li><strong>Backlog Status:</strong> {'Critical accumulation detected' if has_backlog else 'Within normal parameters'}</li>
#         <li><strong>Net Intake:</strong> {'Positive pressure - system accumulating' if net_intake > 0 else 'Negative - system relieving'}</li>
#     </ul>
# </div>
# """, unsafe_allow_html=True)

# if stress_level >= 5 or has_backlog:
#     recommendation = "URGENT: Expand HHS capacity and accelerate discharge procedures. System showing sustained strain."
#     rec_color = "#EF4444"
# elif stress_level >= 3 or net_intake > 5:
#     recommendation = "WARNING: Monitor closely and prepare contingency plans. Moderate pressure detected."
#     rec_color = "#F59E0B"
# else:
#     recommendation = "System operating within sustainable limits. Maintain current operations and continue monitoring."
#     rec_color = "#10B981"

# st.markdown(f"""
# <div style="background: linear-gradient(135deg, rgba({','.join(['239', '68', '68'] if stress_level >= 5 else ['245', '158', '11'] if stress_level >= 3 else ['16', '185', '129'])}, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
#             border-left: 4px solid {rec_color}; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
#     <h4 style="color: {rec_color}; margin-bottom: 0.5rem;">📋 Primary Recommendation</h4>
#     <p style="color: #E2E8F0; font-size: 1.05rem;">{recommendation}</p>
# </div>
# """, unsafe_allow_html=True)

# # ============================================================
# # SECTION 9: SUMMARY STATISTICS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">📊 Summary Statistics</div>', unsafe_allow_html=True)

# summary_df = pd.DataFrame({
#     "Metric": [
#         "Average Daily Intake (CBP)",
#         "Average CBP Custody Load",
#         "Average HHS Care Load",
#         "Average Daily Transfers",
#         "Average Daily Discharges",
#         "Average Total System Load",
#         "Peak System Load",
#         "Minimum System Load",
#         "Average Net Daily Intake",
#         "Average 14-Day Backlog"
#     ],
#     "Value": [
#         f"{filtered_df['apprehended'].mean():.0f}",
#         f"{filtered_df['in_cbp'].mean():.0f}",
#         f"{filtered_df['in_hhs'].mean():.0f}",
#         f"{filtered_df['transferred'].mean():.0f}",
#         f"{filtered_df['discharged'].mean():.0f}",
#         f"{filtered_df['Total_System_Load'].mean():.0f}",
#         f"{filtered_df['Total_System_Load'].max():.0f}",
#         f"{filtered_df['Total_System_Load'].min():.0f}",
#         f"{filtered_df['Net_Daily_Intake'].mean():+.1f}",
#         f"{filtered_df['Backlog_14d'].mean():.1f}"
#     ]
# })

# st.dataframe(summary_df, use_container_width=True, hide_index=True)

# # ============================================================
# # SECTION 10: DOWNLOADS
# # ============================================================
# st.markdown("---")
# st.markdown('<div class="section-title">💾 Export Data</div>', unsafe_allow_html=True)

# dl_col1, dl_col2, dl_col3 = st.columns(3)

# with dl_col1:
#     forecast_csv = pd.DataFrame({
#         "Date": forecast["ds"],
#         "Forecast": forecast["yhat"],
#         "Lower_Bound": forecast["yhat_lower"],
#         "Upper_Bound": forecast["yhat_upper"]
#     }).to_csv(index=False)
#     st.download_button("⬇️ Download Forecast CSV", forecast_csv, 
#                        f"capacity_forecast_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# with dl_col2:
#     full_csv = filtered_df[["date", "in_cbp", "in_hhs", "transferred", "discharged", 
#                            "Total_System_Load", "Net_Daily_Intake", "Backlog_14d"]].to_csv(index=False)
#     st.download_button("📊 Download Full Data CSV", full_csv,
#                        f"uac_capacity_data_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# with dl_col3:
#     kpi_csv = pd.DataFrame({
#         "KPI": ["Total Children", "Net Intake Pressure", "Load Volatility", "Backlog Rate", "Discharge Ratio"],
#         "Value": [f"{latest['KPI_Total_Load']:.0f}", f"{latest['KPI_Net_Intake']:.2f}",
#                   f"{latest['KPI_Volatility']:.2f}%", f"{latest['KPI_Backlog_Rate']:.2f}", f"{latest['KPI_Discharge_Ratio']:.2f}"],
#         "Status": ["Good" if latest['KPI_Total_Load'] < 1500 else "Warning" if latest['KPI_Total_Load'] < 2000 else "Critical",
#                    "Good" if latest['KPI_Net_Intake'] < 0 else "Warning" if latest['KPI_Net_Intake'] < 10 else "Critical",
#                    "Stable" if latest['KPI_Volatility'] < 5 else "Moderate" if latest['KPI_Volatility'] < 10 else "High",
#                    "Good" if latest['KPI_Backlog_Rate'] < 0 else "Warning" if latest['KPI_Backlog_Rate'] < 5 else "Critical",
#                    "Balanced" if 0.8 <= latest['KPI_Discharge_Ratio'] <= 1.2 else "Imbalanced"]
#     }).to_csv(index=False)
#     st.download_button("📈 Download KPI Summary", kpi_csv,
#                        f"kpi_summary_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# # ============================================================
# # FOOTER
# # ============================================================
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; color: #64748B; padding: 1.5rem; border-top: 1px solid rgba(102, 126, 234, 0.2);">
#     <p style="font-size: 1.1rem; font-weight: 600; color: #94A3B8;">
#         🏥 UAC System Capacity & Care Load Analytics
#     </p>
#     <p>Unified Mentor Project | Built with Streamlit, Prophet & Plotly</p>
#     <p style="font-size: 0.8rem; color: #475569;">
#         Data Source: U.S. Department of Health and Human Services | UAC Program
#     </p>
# </div>
# """, unsafe_allow_html=True)







import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from prophet import Prophet
from datetime import datetime, timedelta
import warnings
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors as rl_colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import base64

warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="UAC System Capacity & Care Load Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Dark Theme
st.markdown("""
<style>
    .main-header { 
        font-size: 2.8rem; 
        font-weight: 800; 
        color: #E2E8F0; 
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .sub-header { 
        font-size: 1.15rem; 
        color: #94A3B8; 
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    .kpi-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 126, 234, 0.3);
        padding: 1.8rem 1.2rem;
        border-radius: 16px;
        color: #E2E8F0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(102, 126, 234, 0.6);
    }
    .kpi-value { 
        font-size: 2.6rem; 
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .kpi-label { 
        font-size: 0.85rem; 
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .kpi-status {
        font-size: 0.8rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
    }
    .status-good { background: rgba(16, 185, 129, 0.2); color: #10B981; }
    .status-warning { background: rgba(245, 158, 11, 0.2); color: #F59E0B; }
    .status-danger { background: rgba(239, 68, 68, 0.2); color: #EF4444; }
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #E2E8F0;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
        padding-left: 1.2rem;
        border-left: 4px solid #667eea;
    }
    .section-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 1.5rem;
        padding-left: 1.2rem;
    }
    .alert-box { 
        padding: 1.2rem; 
        border-radius: 12px; 
        margin: 1rem 0; 
        border-left: 4px solid;
        background: rgba(15, 23, 42, 0.8);
    }
    .alert-danger { border-color: #EF4444; }
    .alert-warning { border-color: #F59E0B; }
    .alert-success { border-color: #10B981; }
    .alert-info { border-color: #3B82F6; }
    .insight-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .stress-meter {
        height: 8px;
        border-radius: 4px;
        background: linear-gradient(90deg, #10B981 0%, #F59E0B 50%, #EF4444 100%);
        position: relative;
    }
    .stress-marker {
        width: 4px;
        height: 16px;
        background: white;
        position: absolute;
        top: -4px;
        border-radius: 2px;
        box-shadow: 0 0 10px rgba(255,255,255,0.5);
    }
    .auto-alert {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">🏥 System Capacity & Care Load Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Unaccompanied Children (UAC) Program | Real-Time Capacity Monitoring & Stress Detection</div>', unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data(ttl=3600)
def load_data():
    possible_paths = [
        "data/HHS_Unaccompanied_Alien_Children_Program.csv",
        "../data/HHS_Unaccompanied_Alien_Children_Program.csv",
        "HHS_Unaccompanied_Alien_Children_Program.csv",
        "data/uac_capacity_data.csv",
        "../data/uac_capacity_data.csv"
    ]

    df = None
    used_path = None

    for path in possible_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                used_path = path
                break
            except Exception:
                continue

    if df is not None:
        st.success(f"✅ Data loaded from: {used_path}")

        col_mapping = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if 'date' in col_lower:
                col_mapping[col] = 'date'
            elif 'transferred out' in col_lower:
                col_mapping[col] = 'transferred'
            elif 'discharged' in col_lower:
                col_mapping[col] = 'discharged'
            elif 'apprehended' in col_lower or 'placed in cbp' in col_lower:
                col_mapping[col] = 'apprehended'
            elif 'in cbp' in col_lower or 'cbp custody' in col_lower:
                col_mapping[col] = 'in_cbp'
            elif 'in hhs' in col_lower or 'hhs care' in col_lower:
                col_mapping[col] = 'in_hhs'

        df = df.rename(columns=col_mapping)
        df["date"] = pd.to_datetime(df["date"])

        if df.columns.duplicated().any():
            df = df.loc[:, ~df.columns.duplicated()]

        for col in ["apprehended", "in_cbp", "transferred", "in_hhs", "discharged"]:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: pd.to_numeric(str(x).replace(',', '').replace('$', '').strip(), errors='coerce')
                )

        required_cols = ["date", "apprehended", "in_cbp", "transferred", "in_hhs", "discharged"]
        available_cols = [c for c in required_cols if c in df.columns]

        df = df[available_cols].dropna().sort_values("date").reset_index(drop=True)
        return df

    st.info("📊 Using synthetic data for demonstration...")
    dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq="D")
    np.random.seed(42)
    n_days = len(dates)

    day_of_year = dates.dayofyear
    seasonal = 1 + 0.35 * np.sin(2 * np.pi * (day_of_year - 60) / 365)
    policy_effect = np.ones(n_days)
    policy_effect[400:450] = 0.6
    policy_effect[700:750] = 1.4

    trend = np.linspace(1.0, 1.2, n_days)

    base_intake = (120 * seasonal * trend * policy_effect + np.random.normal(0, 20, n_days)).astype(int)
    base_intake = np.maximum(base_intake, 15)

    cbp = np.zeros(n_days)
    cbp[0] = base_intake[0]
    for i in range(1, n_days):
        outflow = int(cbp[i-1] * np.random.uniform(0.2, 0.4))
        cbp[i] = max(0, min(2500, cbp[i-1] + base_intake[i] - outflow))

    transfers = np.minimum(
        (cbp * np.random.uniform(0.5, 0.85, n_days) + np.random.normal(0, 8, n_days)).astype(int),
        cbp
    )
    transfers = np.maximum(transfers, 0)

    hhs = np.zeros(n_days)
    hhs[0] = transfers[0]
    for i in range(1, n_days):
        discharge_rate = np.random.uniform(0.06, 0.2)
        discharges_today = int(hhs[i-1] * discharge_rate)
        hhs[i] = max(0, hhs[i-1] + transfers[i] - discharges_today)

    discharges = np.zeros(n_days)
    for i in range(1, n_days):
        discharge_rate = np.random.uniform(0.06, 0.2)
        discharges[i] = int(hhs[i-1] * discharge_rate)
    discharges = np.minimum(discharges, hhs)

    df = pd.DataFrame({
        "date": dates,
        "apprehended": base_intake.astype(int),
        "in_cbp": cbp.astype(int),
        "transferred": transfers.astype(int),
        "in_hhs": hhs.astype(int),
        "discharged": discharges.astype(int)
    })
    return df

df = load_data()

# ============================================================
# BACKEND LOGIC - DERIVED HEALTHCARE CAPACITY METRICS
# ============================================================

df["Total_System_Load"] = df["in_cbp"] + df["in_hhs"]
df["Net_Daily_Intake"] = df["transferred"] - df["discharged"]
df["Growth_Rate"] = df["Total_System_Load"].pct_change() * 100

df["Load_Rolling_7d"] = df["Total_System_Load"].rolling(window=7, min_periods=1).mean()
df["Load_Rolling_14d"] = df["Total_System_Load"].rolling(window=14, min_periods=1).mean()
df["CBP_Rolling_7d"] = df["in_cbp"].rolling(window=7, min_periods=1).mean()
df["CBP_Rolling_14d"] = df["in_cbp"].rolling(window=14, min_periods=1).mean()
df["HHS_Rolling_7d"] = df["in_hhs"].rolling(window=7, min_periods=1).mean()
df["HHS_Rolling_14d"] = df["in_hhs"].rolling(window=14, min_periods=1).mean()

df["Backlog_7d"] = df["Net_Daily_Intake"].rolling(window=7, min_periods=1).sum()
df["Backlog_14d"] = df["Net_Daily_Intake"].rolling(window=14, min_periods=1).sum()

df["Load_Volatility"] = df["Total_System_Load"].rolling(window=14, min_periods=1).std()
df["CBP_Volatility"] = df["in_cbp"].rolling(window=7, min_periods=1).std()
df["HHS_Volatility"] = df["in_hhs"].rolling(window=7, min_periods=1).std()

df["Stress_Flag"] = df["Total_System_Load"] > df["Load_Rolling_14d"] * 1.1
df["Sustained_Stress"] = df["Stress_Flag"].rolling(window=7, min_periods=1).sum()

df["KPI_Total_Load"] = df["Total_System_Load"]
df["KPI_Net_Intake"] = df["Net_Daily_Intake"].rolling(window=7, min_periods=1).mean()
df["KPI_Volatility"] = (df["Load_Volatility"] / df["Total_System_Load"].rolling(window=14, min_periods=1).mean()) * 100
df["KPI_Backlog_Rate"] = df["Backlog_14d"] / 14
df["KPI_Discharge_Ratio"] = df["discharged"] / df["transferred"].replace(0, np.nan)

df = df.fillna(0)

# ============================================================
# SIDEBAR - CONTROL PANEL
# ============================================================
st.sidebar.markdown("## ⚙️ Control Panel")
st.sidebar.markdown("---")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

mask = (df["date"] >= pd.Timestamp(start_date)) & (df["date"] <= pd.Timestamp(end_date))
filtered_df = df[mask].copy()

st.sidebar.markdown("---")

granularity = st.sidebar.selectbox("⏱️ Time Granularity", ["Daily", "Weekly", "Monthly"], index=0)

if granularity == "Weekly":
    filtered_df = filtered_df.set_index("date").resample("W").mean().reset_index()
    filtered_df["date"] = filtered_df["date"].dt.to_period("W").dt.start_time
elif granularity == "Monthly":
    filtered_df = filtered_df.set_index("date").resample("M").mean().reset_index()
    filtered_df["date"] = filtered_df["date"].dt.to_period("M").dt.start_time

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Display Options")
show_cbp = st.sidebar.checkbox("Show CBP Load", value=True)
show_hhs = st.sidebar.checkbox("Show HHS Load", value=True)
show_total = st.sidebar.checkbox("Show Total System Load", value=True)
show_rolling = st.sidebar.checkbox("Show Rolling Averages", value=True)
show_stress = st.sidebar.checkbox("Highlight Stress Periods", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔮 Forecast")
forecast_days = st.sidebar.slider("Forecast Days", 30, 365, 90)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔔 Auto Alerts")
alert_threshold = st.sidebar.number_input("Capacity Alert Threshold", min_value=1000, max_value=20000, value=8000)
enable_alerts = st.sidebar.checkbox("Enable Auto Alerts", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Period Comparison")
compare_periods = st.sidebar.checkbox("Compare Two Periods", value=False)
if compare_periods:
    st.sidebar.markdown("**Period 1 (Current)**")
    p1_start = st.sidebar.date_input("P1 Start", min_date, min_value=min_date, max_value=max_date)
    p1_end = st.sidebar.date_input("P1 End", min_date + timedelta(days=90), min_value=min_date, max_value=max_date)
    st.sidebar.markdown("**Period 2 (Compare)**")
    p2_start = st.sidebar.date_input("P2 Start", max_date - timedelta(days=180), min_value=min_date, max_value=max_date)
    p2_end = st.sidebar.date_input("P2 End", max_date, min_value=min_date, max_value=max_date)

# ============================================================
# AUTO ALERTS SECTION
# ============================================================
if enable_alerts:
    latest = filtered_df.iloc[-1] if len(filtered_df) > 0 else df.iloc[-1]

    alerts = []
    if latest["Total_System_Load"] > alert_threshold:
        alerts.append(("🚨 CAPACITY ALERT", f"System load ({int(latest['Total_System_Load'])}) exceeds threshold ({alert_threshold})", "danger"))
    if latest["Sustained_Stress"] >= 5:
        alerts.append(("🔥 STRESS ALERT", f"Sustained stress for {int(latest['Sustained_Stress'])} days", "danger"))
    if latest["Backlog_14d"] > 100:
        alerts.append(("📈 BACKLOG ALERT", f"14-day backlog accumulation: {int(latest['Backlog_14d'])}", "warning"))
    if latest["KPI_Net_Intake"] > 50:
        alerts.append(("⚠️ INTAKE PRESSURE", f"High net intake: {latest['KPI_Net_Intake']:.1f} children/day", "warning"))

    if alerts:
        st.markdown("---")
        st.markdown('<div class="section-title">🚨 Active Alerts</div>', unsafe_allow_html=True)
        for title, message, level in alerts:
            color = "#EF4444" if level == "danger" else "#F59E0B"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba({','.join(['239', '68', '68'] if level == 'danger' else ['245', '158', '11'])}, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%);
                        border-left: 4px solid {color}; padding: 1rem 1.5rem; border-radius: 12px; margin: 0.5rem 0;">
                <strong style="color: {color}; font-size: 1.1rem;">{title}</strong>
                <p style="color: #E2E8F0; margin: 0.3rem 0 0 0;">{message}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# LATEST DATA FOR KPIs
# ============================================================
latest = filtered_df.iloc[-1] if len(filtered_df) > 0 else df.iloc[-1]

stress_level = latest["Sustained_Stress"]
if stress_level >= 5:
    stress_status = "CRITICAL"
    stress_class = "status-danger"
elif stress_level >= 3:
    stress_status = "ELEVATED"
    stress_class = "status-warning"
else:
    stress_status = "NORMAL"
    stress_class = "status-good"

backlog_trend = latest["Backlog_14d"]
if backlog_trend > 50:
    backlog_status = "ACCUMULATING"
    backlog_class = "status-danger"
elif backlog_trend > 0:
    backlog_status = "GROWING"
    backlog_class = "status-warning"
else:
    backlog_status = "STABLE"
    backlog_class = "status-good"

# ============================================================
# SECTION 1: KPI SUMMARY CARDS
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">📊 System Capacity Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Real-time monitoring of total care load, intake pressure, and system stress levels</div>', unsafe_allow_html=True)

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    total_load = int(latest["KPI_Total_Load"])
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total_load:,}</div>
        <div class="kpi-label">Total Children Under Care</div>
        <div class="kpi-status {stress_class}">{stress_status}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    daily_intake = int(latest["transferred"])
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{daily_intake:,}</div>
        <div class="kpi-label">Daily Intake (Transfers)</div>
        <div class="kpi-status status-info">Into HHS System</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    daily_outflow = int(latest["discharged"])
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{daily_outflow:,}</div>
        <div class="kpi-label">Daily Outflow (Discharges)</div>
        <div class="kpi-status status-info">To Sponsors</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    net_intake = latest["KPI_Net_Intake"]
    pressure_color = "status-danger" if net_intake > 10 else "status-warning" if net_intake > 0 else "status-good"
    pressure_text = "HIGH PRESSURE" if net_intake > 10 else "MODERATE" if net_intake > 0 else "BALANCED"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{net_intake:+.0f}</div>
        <div class="kpi-label">Net Intake Pressure</div>
        <div class="kpi-status {pressure_color}">{pressure_text}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# STRESS METER
# ============================================================
st.markdown("---")
stress_col1, stress_col2 = st.columns([3, 1])

with stress_col1:
    st.markdown('<div class="section-title">🔥 System Stress Indicator</div>', unsafe_allow_html=True)
    current_stress = min(stress_level / 7 * 100, 100)
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.8); padding: 1.5rem; border-radius: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #10B981; font-weight: 600;">Normal</span>
            <span style="color: #F59E0B; font-weight: 600;">Elevated</span>
            <span style="color: #EF4444; font-weight: 600;">Critical</span>
        </div>
        <div class="stress-meter">
            <div class="stress-marker" style="left: {current_stress}%;"></div>
        </div>
        <div style="text-align: center; margin-top: 1rem; color: #94A3B8;">
            Current Stress Level: <strong style="color: {'#EF4444' if stress_level >= 5 else '#F59E0B' if stress_level >= 3 else '#10B981'};">{stress_level}/7 days</strong> sustained pressure
        </div>
    </div>
    """, unsafe_allow_html=True)

with stress_col2:
    st.markdown('<div class="section-title">📈 Backlog Trend</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.8); padding: 1.5rem; border-radius: 12px; text-align: center;">
        <div style="font-size: 2.2rem; font-weight: 800; color: {'#EF4444' if backlog_trend > 50 else '#F59E0B' if backlog_trend > 0 else '#10B981'};">{backlog_trend:+.0f}</div>
        <div style="color: #94A3B8; font-size: 0.9rem;">14-Day Accumulation</div>
        <div class="kpi-status {backlog_class}" style="margin-top: 0.8rem;">{backlog_status}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# SECTION 2: TIME SERIES ANALYSIS
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">📈 Time Series Analysis: System Load & Pressure Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">When the daily load (solid line) rises above the 14-day rolling average (dashed), the system enters a stress period</div>', unsafe_allow_html=True)

fig_load = go.Figure()

if show_total:
    fig_load.add_trace(go.Scatter(
        x=filtered_df["date"], y=filtered_df["Total_System_Load"],
        mode="lines", name="Total System Load",
        line=dict(color="#667eea", width=2),
        fill="tozeroy", fillcolor="rgba(102, 126, 234, 0.08)",
        hovertemplate="<b>Total Load</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>"
    ))

if show_cbp:
    fig_load.add_trace(go.Scatter(
        x=filtered_df["date"], y=filtered_df["in_cbp"],
        mode="lines", name="CBP Custody",
        line=dict(color="#f5576c", width=1.5),
        hovertemplate="<b>CBP</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>"
    ))

if show_hhs:
    fig_load.add_trace(go.Scatter(
        x=filtered_df["date"], y=filtered_df["in_hhs"],
        mode="lines", name="HHS Care",
        line=dict(color="#11998e", width=1.5),
        hovertemplate="<b>HHS</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>"
    ))

if show_rolling:
    fig_load.add_trace(go.Scatter(
        x=filtered_df["date"], y=filtered_df["Load_Rolling_7d"],
        mode="lines", name="7-Day Rolling Avg",
        line=dict(color="#F59E0B", width=2, dash="dash"),
        hovertemplate="<b>7-Day Avg</b><br>Date: %{x}<br>Avg: %{y:,.0f}<extra></extra>"
    ))
    fig_load.add_trace(go.Scatter(
        x=filtered_df["date"], y=filtered_df["Load_Rolling_14d"],
        mode="lines", name="14-Day Rolling Avg",
        line=dict(color="#EF4444", width=2, dash="dot"),
        hovertemplate="<b>14-Day Avg</b><br>Date: %{x}<br>Avg: %{y:,.0f}<extra></extra>"
    ))

if show_stress:
    stress_df = filtered_df[filtered_df["Stress_Flag"] == True]
    if len(stress_df) > 0:
        fig_load.add_trace(go.Scatter(
            x=stress_df["date"], y=stress_df["Total_System_Load"],
            mode="markers", name="⚠️ Stress Period",
            marker=dict(color="#EF4444", size=8, symbol="diamond"),
            hovertemplate="<b>STRESS ALERT</b><br>Date: %{x}<br>Load: %{y:,.0f}<extra></extra>"
        ))

if enable_alerts:
    fig_load.add_hline(y=alert_threshold, line_dash="dash", line_color="#EF4444", opacity=0.7,
                        annotation_text=f"Alert ({alert_threshold})", annotation_position="top right")

fig_load.update_layout(
    height=500,
    template="plotly_dark",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    yaxis_title="Number of Children",
    xaxis_title="Date",
    hovermode="x unified"
)

st.plotly_chart(fig_load, use_container_width=True)

# ============================================================
# SECTION 3: PERIOD COMPARISON
# ============================================================
if compare_periods:
    st.markdown("---")
    st.markdown('<div class="section-title">📅 Period Comparison Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Compare capacity metrics between two time periods</div>', unsafe_allow_html=True)

    p1_mask = (df["date"] >= pd.Timestamp(p1_start)) & (df["date"] <= pd.Timestamp(p1_end))
    p2_mask = (df["date"] >= pd.Timestamp(p2_start)) & (df["date"] <= pd.Timestamp(p2_end))
    p1_df = df[p1_mask]
    p2_df = df[p2_mask]

    if len(p1_df) > 0 and len(p2_df) > 0:
        comp_metrics = {
            "Metric": ["Avg Total Load", "Avg CBP Load", "Avg HHS Load", "Avg Transfers", "Avg Discharges", "Peak Load", "Stress Days"],
            f"Period 1 ({p1_start} to {p1_end})": [
                f"{p1_df['Total_System_Load'].mean():.0f}",
                f"{p1_df['in_cbp'].mean():.0f}",
                f"{p1_df['in_hhs'].mean():.0f}",
                f"{p1_df['transferred'].mean():.0f}",
                f"{p1_df['discharged'].mean():.0f}",
                f"{p1_df['Total_System_Load'].max():.0f}",
                f"{p1_df['Stress_Flag'].sum():.0f}"
            ],
            f"Period 2 ({p2_start} to {p2_end})": [
                f"{p2_df['Total_System_Load'].mean():.0f}",
                f"{p2_df['in_cbp'].mean():.0f}",
                f"{p2_df['in_hhs'].mean():.0f}",
                f"{p2_df['transferred'].mean():.0f}",
                f"{p2_df['discharged'].mean():.0f}",
                f"{p2_df['Total_System_Load'].max():.0f}",
                f"{p2_df['Stress_Flag'].sum():.0f}"
            ],
            "Change": [
                f"{((p2_df['Total_System_Load'].mean() - p1_df['Total_System_Load'].mean()) / p1_df['Total_System_Load'].mean() * 100):+.1f}%",
                f"{((p2_df['in_cbp'].mean() - p1_df['in_cbp'].mean()) / p1_df['in_cbp'].mean() * 100):+.1f}%",
                f"{((p2_df['in_hhs'].mean() - p1_df['in_hhs'].mean()) / p1_df['in_hhs'].mean() * 100):+.1f}%",
                f"{((p2_df['transferred'].mean() - p1_df['transferred'].mean()) / p1_df['transferred'].mean() * 100):+.1f}%",
                f"{((p2_df['discharged'].mean() - p1_df['discharged'].mean()) / p1_df['discharged'].mean() * 100):+.1f}%",
                f"{((p2_df['Total_System_Load'].max() - p1_df['Total_System_Load'].max()) / p1_df['Total_System_Load'].max() * 100):+.1f}%",
                f"{p2_df['Stress_Flag'].sum() - p1_df['Stress_Flag'].sum():+.0f}"
            ]
        }
        st.dataframe(pd.DataFrame(comp_metrics), use_container_width=True, hide_index=True)

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=["Total Load", "CBP", "HHS", "Transfers", "Discharges"],
            y=[p1_df['Total_System_Load'].mean(), p1_df['in_cbp'].mean(), p1_df['in_hhs'].mean(), 
               p1_df['transferred'].mean(), p1_df['discharged'].mean()],
            name=f"Period 1", marker_color="#667eea"
        ))
        fig_comp.add_trace(go.Bar(
            x=["Total Load", "CBP", "HHS", "Transfers", "Discharges"],
            y=[p2_df['Total_System_Load'].mean(), p2_df['in_cbp'].mean(), p2_df['in_hhs'].mean(),
               p2_df['transferred'].mean(), p2_df['discharged'].mean()],
            name=f"Period 2", marker_color="#10B981"
        ))
        fig_comp.update_layout(
            height=400, template="plotly_dark", barmode="group",
            title="Average Metrics Comparison"
        )
        st.plotly_chart(fig_comp, use_container_width=True)

# ============================================================
# SECTION 4: SYSTEM BALANCE
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">⚖️ System Balance: Intake vs Discharge Gap</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Persistent positive gap indicates backlog accumulation and capacity strain</div>', unsafe_allow_html=True)

fig_balance = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Net Daily Intake (Transfers - Discharges)", "14-Day Backlog Accumulation Trend"),
    vertical_spacing=0.15
)

# FIX: Renamed 'colors' to 'bar_colors' to avoid shadowing reportlab.colors
bar_colors = ["#10B981" if x < 0 else "#EF4444" if x > 10 else "#F59E0B" for x in filtered_df["Net_Daily_Intake"]]
fig_balance.add_trace(go.Bar(
    x=filtered_df["date"], y=filtered_df["Net_Daily_Intake"],
    name="Net Intake", marker_color=bar_colors, opacity=0.8,
    hovertemplate="<b>Net Intake</b><br>Date: %{x}<br>Value: %{y:+.0f}<extra></extra>"
), row=1, col=1)

fig_balance.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
fig_balance.add_hline(y=10, line_dash="dot", line_color="#EF4444", row=1, col=1,
                       annotation_text="Critical Threshold", annotation_position="top right")

fig_balance.add_trace(go.Scatter(
    x=filtered_df["date"], y=filtered_df["Backlog_14d"],
    mode="lines", name="14-Day Backlog", fill="tozeroy",
    line=dict(color="#667eea", width=2),
    fillcolor="rgba(102, 126, 234, 0.15)",
    hovertemplate="<b>14-Day Backlog</b><br>Date: %{x}<br>Accumulation: %{y:+.0f}<extra></extra>"
), row=2, col=1)

fig_balance.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)

fig_balance.update_layout(
    height=650,
    template="plotly_dark",
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_balance, use_container_width=True)

# ============================================================
# SECTION 5: PRESSURE & STRESS IDENTIFICATION
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">🔍 Pressure & Stress Identification</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Rolling averages and variability analysis to detect prolonged strain windows</div>', unsafe_allow_html=True)

fig_stress = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "CBP: 7-Day vs 14-Day Rolling Average",
        "HHS: 7-Day vs 14-Day Rolling Average",
        "CBP Load Variability (7d Std Dev)",
        "HHS Load Variability (7d Std Dev)"
    ),
    vertical_spacing=0.12, horizontal_spacing=0.08
)

fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["CBP_Rolling_7d"], 
               mode="lines", name="CBP 7d", line=dict(color="#f5576c")), row=1, col=1)
fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["CBP_Rolling_14d"], 
               mode="lines", name="CBP 14d", line=dict(color="#f093fb", dash="dash")), row=1, col=1)

fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["HHS_Rolling_7d"], 
               mode="lines", name="HHS 7d", line=dict(color="#11998e")), row=1, col=2)
fig_stress.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["HHS_Rolling_14d"], 
               mode="lines", name="HHS 14d", line=dict(color="#38ef7d", dash="dash")), row=1, col=2)

fig_stress.add_trace(go.Bar(x=filtered_df["date"], y=filtered_df["CBP_Volatility"], 
           marker_color="#f5576c", opacity=0.6, name="CBP Volatility"), row=2, col=1)
fig_stress.add_trace(go.Bar(x=filtered_df["date"], y=filtered_df["HHS_Volatility"], 
           marker_color="#11998e", opacity=0.6, name="HHS Volatility"), row=2, col=2)

fig_stress.update_layout(height=650, template="plotly_dark", showlegend=False)
st.plotly_chart(fig_stress, use_container_width=True)

# ============================================================
# SECTION 6: CAPACITY DISTRIBUTION & FLOW
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">🏛️ Capacity Distribution & Flow Analysis</div>', unsafe_allow_html=True)

fig_dist = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "pie"}, {"type": "xy"}]],
    subplot_titles=("Current Load Distribution", "Transfer vs Discharge Flow")
)

latest_data = filtered_df.iloc[-1] if len(filtered_df) > 0 else df.iloc[-1]

fig_dist.add_trace(go.Pie(
    labels=["CBP Custody", "HHS Care"],
    values=[latest_data["in_cbp"], latest_data["in_hhs"]],
    hole=0.55,
    marker_colors=["#f5576c", "#11998e"],
    textinfo="label+percent",
    textfont=dict(size=12, color="white")
), row=1, col=1)

fig_dist.add_trace(go.Scatter(
    x=filtered_df["date"], y=filtered_df["transferred"],
    mode="lines", name="Transfers to HHS", line=dict(color="#667eea", width=2),
    fill="tozeroy", fillcolor="rgba(102, 126, 234, 0.15)"
), row=1, col=2)

fig_dist.add_trace(go.Scatter(
    x=filtered_df["date"], y=filtered_df["discharged"],
    mode="lines", name="Discharges from HHS", line=dict(color="#10B981", width=2),
    fill="tozeroy", fillcolor="rgba(16, 185, 129, 0.15)"
), row=1, col=2)

fig_dist.update_layout(height=400, template="plotly_dark", showlegend=True,
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig_dist, use_container_width=True)

# ============================================================
# SECTION 7: AI FORECASTING
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">🔮 AI Forecasting: Total System Load Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Prophet model with changepoint detection for policy shift awareness</div>', unsafe_allow_html=True)

prophet_df = filtered_df[["date", "Total_System_Load"]].rename(columns={"date": "ds", "Total_System_Load": "y"})

policy_changes = pd.DataFrame({
    'holiday': 'policy_change',
    'ds': pd.to_datetime(['2024-03-01', '2024-09-01', '2025-01-01']),
    'lower_window': -15,
    'upper_window': 15
})

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.15,
    seasonality_prior_scale=10.0,
    holidays=policy_changes,
    growth="flat",
    changepoint_range=0.95
)

if len(prophet_df) > 365:
    model.add_seasonality(name="monthly", period=30.5, fourier_order=5)

model.fit(prophet_df)

future = model.make_future_dataframe(periods=forecast_days)
future["floor"] = 0

forecast = model.predict(future)

forecast["yhat"] = np.maximum(forecast["yhat"], 0)
forecast["yhat_lower"] = np.maximum(forecast["yhat_lower"], 0)
forecast["yhat_upper"] = np.maximum(forecast["yhat_upper"], 0)

fig_forecast = go.Figure()
fig_forecast.add_trace(go.Scatter(
    x=prophet_df["ds"], y=prophet_df["y"],
    name="Actual Load", mode="lines", line=dict(color="#3B82F6", width=2)
))
fig_forecast.add_trace(go.Scatter(
    x=forecast["ds"], y=forecast["yhat"],
    name="AI Forecast", mode="lines", line=dict(color="#10B981", width=2)
))
fig_forecast.add_trace(go.Scatter(
    x=forecast["ds"].tolist() + forecast["ds"].tolist()[::-1],
    y=forecast["yhat_upper"].tolist() + forecast["yhat_lower"].tolist()[::-1],
    fill="toself", fillcolor="rgba(16, 185, 129, 0.15)",
    line=dict(color="rgba(255,255,255,0)"), name="Confidence Interval"
))

fig_forecast.add_hline(y=alert_threshold, line_dash="dash", line_color="#EF4444",
                        annotation_text=f"Alert ({alert_threshold})", annotation_position="top right")

fig_forecast.update_layout(
    title=f"Forecast for Total System Load ({forecast_days} days)",
    yaxis_title="Total Children Under Care",
    height=500, template="plotly_dark", hovermode="x unified"
)
st.plotly_chart(fig_forecast, use_container_width=True)

future_value = forecast["yhat"].iloc[-1]
recent_value = forecast["yhat"].iloc[-forecast_days] if len(forecast) > forecast_days else forecast["yhat"].iloc[len(forecast)//2]
trend_change = ((future_value - recent_value) / recent_value * 100) if recent_value > 0 else 0

insight_col1, insight_col2, insight_col3 = st.columns(3)
with insight_col1:
    if trend_change > 10:
        st.error(f"🚨 Capacity Crisis\n+{trend_change:.1f}% predicted")
    elif trend_change > 0:
        st.warning(f"⚠️ Growing Load\n+{trend_change:.1f}% predicted")
    else:
        st.success(f"✅ Capacity Relief\n{trend_change:.1f}% predicted")

with insight_col2:
    peak_date = forecast.loc[forecast["yhat"].idxmax(), "ds"]
    st.info(f"📅 Predicted Peak\n{peak_date.strftime('%B %Y')}")

with insight_col3:
    conf_width = (forecast["yhat_upper"].iloc[-1] - forecast["yhat_lower"].iloc[-1]) / forecast["yhat"].iloc[-1] * 100
    st.success(f"✅ Confidence\n±{conf_width/2:.1f}% uncertainty")

# ============================================================
# SECTION 8: DATA QUALITY & ANOMALIES
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">🔍 Data Quality & Logical Constraint Validation</div>', unsafe_allow_html=True)

violations = []
for idx, row in filtered_df.iterrows():
    if row["transferred"] > (row["in_cbp"] + row["transferred"]):
        violations.append({"Date": row["date"], "Type": "Transfer exceeds total CBP flow", "Severity": "Critical"})
    if row["discharged"] > row["in_hhs"]:
        violations.append({"Date": row["date"], "Type": "Discharge > HHS Care", "Severity": "Critical"})
    if any(row[col] < 0 for col in ["in_cbp", "in_hhs", "transferred", "discharged"]):
        violations.append({"Date": row["date"], "Type": "Negative value detected", "Severity": "Warning"})
    if row["Total_System_Load"] > (df["Total_System_Load"].mean() + 3 * df["Total_System_Load"].std()):
        violations.append({"Date": row["date"], "Type": "Extreme outlier load", "Severity": "Warning"})

if violations:
    st.warning(f"⚠️ {len(violations)} data quality issues detected")
    st.dataframe(pd.DataFrame(violations), use_container_width=True)
else:
    st.success("✅ All logical constraints validated successfully")

# ============================================================
# SECTION 9: EXECUTIVE INSIGHTS
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">💡 Executive Insights & Recommendations</div>', unsafe_allow_html=True)

stress_periods = []
in_stress = False
start_date_stress = None
for idx, row in filtered_df.iterrows():
    if row["Stress_Flag"] and not in_stress:
        in_stress = True
        start_date_stress = row["date"]
    elif not row["Stress_Flag"] and in_stress:
        in_stress = False
        if start_date_stress:
            duration = (row["date"] - start_date_stress).days if hasattr(row["date"], 'days') else 1
            if duration >= 3:
                stress_periods.append(f"{start_date_stress.strftime('%Y-%m-%d')} to {row['date'].strftime('%Y-%m-%d')} ({duration} days)")

sustained_backlog = filtered_df[filtered_df["Backlog_14d"] > 50]
has_backlog = latest["Backlog_14d"] > 50

st.markdown(f"""
<div class="insight-card">
    <h4 style="color: #E2E8F0; margin-bottom: 1rem;">🎯 Key Findings</h4>
    <ul style="color: #CBD5E1; line-height: 2;">
        <li><strong>System Load:</strong> Currently <span style="color: {'#EF4444' if total_load > alert_threshold else '#10B981'};">{total_load:,} children</span> under care</li>
        <li><strong>Stress Periods:</strong> {len(stress_periods)} sustained high-load periods detected in selected range</li>
        <li><strong>Backlog Status:</strong> {'Critical accumulation detected' if has_backlog else 'Within normal parameters'}</li>
        <li><strong>Net Intake:</strong> {'Positive pressure - system accumulating' if net_intake > 0 else 'Negative - system relieving'}</li>
        <li><strong>Forecast Trend:</strong> {'Increasing' if trend_change > 0 else 'Decreasing'} ({trend_change:+.1f}%)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

if stress_level >= 5 or has_backlog or total_load > alert_threshold:
    recommendation = "URGENT: Expand HHS capacity and accelerate discharge procedures. System showing sustained strain."
    rec_color = "#EF4444"
elif stress_level >= 3 or net_intake > 5:
    recommendation = "WARNING: Monitor closely and prepare contingency plans. Moderate pressure detected."
    rec_color = "#F59E0B"
else:
    recommendation = "System operating within sustainable limits. Maintain current operations and continue monitoring."
    rec_color = "#10B981"

st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba({','.join(['239', '68', '68'] if stress_level >= 5 or total_load > alert_threshold else ['245', '158', '11'] if stress_level >= 3 else ['16', '185', '129'])}, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
            border-left: 4px solid {rec_color}; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
    <h4 style="color: {rec_color}; margin-bottom: 0.5rem;">📋 Primary Recommendation</h4>
    <p style="color: #E2E8F0; font-size: 1.05rem;">{recommendation}</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 10: SUMMARY STATISTICS
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">📊 Summary Statistics</div>', unsafe_allow_html=True)

summary_df = pd.DataFrame({
    "Metric": [
        "Average Daily Intake (CBP)",
        "Average CBP Custody Load",
        "Average HHS Care Load",
        "Average Daily Transfers",
        "Average Daily Discharges",
        "Average Total System Load",
        "Peak System Load",
        "Minimum System Load",
        "Average Net Daily Intake",
        "Average 14-Day Backlog"
    ],
    "Value": [
        f"{filtered_df['apprehended'].mean():.0f}",
        f"{filtered_df['in_cbp'].mean():.0f}",
        f"{filtered_df['in_hhs'].mean():.0f}",
        f"{filtered_df['transferred'].mean():.0f}",
        f"{filtered_df['discharged'].mean():.0f}",
        f"{filtered_df['Total_System_Load'].mean():.0f}",
        f"{filtered_df['Total_System_Load'].max():.0f}",
        f"{filtered_df['Total_System_Load'].min():.0f}",
        f"{filtered_df['Net_Daily_Intake'].mean():+.1f}",
        f"{filtered_df['Backlog_14d'].mean():.1f}"
    ]
})

st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ============================================================
# SECTION 11: PDF REPORT GENERATOR (FIXED)
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">📄 Generate Executive Report</div>', unsafe_allow_html=True)

def generate_pdf_report():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=rl_colors.HexColor('#667eea'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=rl_colors.HexColor('#764ba2'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=rl_colors.HexColor('#333333'),
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    story = []

    story.append(Paragraph("UAC System Capacity & Care Load Analytics", title_style))
    story.append(Paragraph(f"Executive Report - Generated: {datetime.now().strftime('%B %d, %Y')}", body_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(f"""
    This report analyzes the capacity and care load of the Unaccompanied Children (UAC) Program 
    from {start_date} to {end_date}. The system currently cares for <b>{total_load:,} children</b> 
    with a stress level classified as <b>{stress_status}</b>.
    """, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Key Performance Indicators", heading_style))
    kpi_data = [
        ["Metric", "Value", "Status"],
        ["Total Children Under Care", f"{total_load:,}", stress_status],
        ["Daily Intake (Transfers)", f"{daily_intake:,}", "Active"],
        ["Daily Outflow (Discharges)", f"{daily_outflow:,}", "Active"],
        ["Net Intake Pressure", f"{net_intake:+.0f}", pressure_text],
        ["14-Day Backlog", f"{backlog_trend:+.0f}", backlog_status]
    ]

    kpi_table = Table(kpi_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), rl_colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, rl_colors.HexColor('#dee2e6')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [rl_colors.HexColor('#f8f9fa'), rl_colors.white])
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Key Findings", heading_style))
    findings = f"""
    <ul>
        <li>System Load: Currently <b>{total_load:,} children</b> under care</li>
        <li>Stress Periods: {len(stress_periods)} sustained high-load periods detected</li>
        <li>Backlog Status: {'Critical accumulation detected' if has_backlog else 'Within normal parameters'}</li>
        <li>Net Intake: {'Positive pressure - system accumulating' if net_intake > 0 else 'Negative - system relieving'}</li>
        <li>Forecast Trend: {'Increasing' if trend_change > 0 else 'Decreasing'} ({trend_change:+.1f}%)</li>
    </ul>
    """
    story.append(Paragraph(findings, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Primary Recommendation", heading_style))
    story.append(Paragraph(f"<b>Status:</b> {rec_color.replace('#', '')}<br/>{recommendation}", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Summary Statistics", heading_style))
    stats_data = [["Metric", "Value"]] + [[row["Metric"], row["Value"]] for _, row in summary_df.iterrows()]
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#764ba2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, rl_colors.HexColor('#dee2e6')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [rl_colors.HexColor('#f8f9fa'), rl_colors.white])
    ]))
    story.append(stats_table)

    story.append(Spacer(1, 30))
    story.append(Paragraph("""
    <hr/>
    <p align="center" style="font-size: 8pt; color: #666;">
    UAC System Capacity & Care Load Analytics | Unified Mentor Project<br/>
    Data Source: U.S. Department of Health and Human Services | UAC Program<br/>
    Generated automatically from Streamlit Dashboard
    </p>
    """, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

if st.button("📄 Generate PDF Report"):
    with st.spinner("Generating executive report..."):
        pdf_buffer = generate_pdf_report()
        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_buffer,
            file_name=f"UAC_Capacity_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        st.success("✅ Report generated successfully!")

# ============================================================
# SECTION 12: DOWNLOADS
# ============================================================
st.markdown("---")
st.markdown('<div class="section-title">💾 Export Data</div>', unsafe_allow_html=True)

dl_col1, dl_col2, dl_col3 = st.columns(3)

with dl_col1:
    forecast_csv = pd.DataFrame({
        "Date": forecast["ds"],
        "Forecast": forecast["yhat"],
        "Lower_Bound": forecast["yhat_lower"],
        "Upper_Bound": forecast["yhat_upper"]
    }).to_csv(index=False)
    st.download_button("⬇️ Download Forecast CSV", forecast_csv, 
                       f"capacity_forecast_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

with dl_col2:
    full_csv = filtered_df[["date", "in_cbp", "in_hhs", "transferred", "discharged", 
                           "Total_System_Load", "Net_Daily_Intake", "Backlog_14d"]].to_csv(index=False)
    st.download_button("📊 Download Full Data CSV", full_csv,
                       f"uac_capacity_data_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

with dl_col3:
    kpi_csv = pd.DataFrame({
        "KPI": ["Total Children", "Net Intake Pressure", "Load Volatility", "Backlog Rate", "Discharge Ratio"],
        "Value": [f"{latest['KPI_Total_Load']:.0f}", f"{latest['KPI_Net_Intake']:.2f}",
                  f"{latest['KPI_Volatility']:.2f}%", f"{latest['KPI_Backlog_Rate']:.2f}", f"{latest['KPI_Discharge_Ratio']:.2f}"],
        "Status": ["Good" if latest['KPI_Total_Load'] < alert_threshold else "Warning" if latest['KPI_Total_Load'] < alert_threshold * 1.25 else "Critical",
                   "Good" if latest['KPI_Net_Intake'] < 0 else "Warning" if latest['KPI_Net_Intake'] < 10 else "Critical",
                   "Stable" if latest['KPI_Volatility'] < 5 else "Moderate" if latest['KPI_Volatility'] < 10 else "High",
                   "Good" if latest['KPI_Backlog_Rate'] < 0 else "Warning" if latest['KPI_Backlog_Rate'] < 5 else "Critical",
                   "Balanced" if 0.8 <= latest['KPI_Discharge_Ratio'] <= 1.2 else "Imbalanced"]
    }).to_csv(index=False)
    st.download_button("📈 Download KPI Summary", kpi_csv,
                       f"kpi_summary_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; padding: 1.5rem; border-top: 1px solid rgba(102, 126, 234, 0.2);">
    <p style="font-size: 1.1rem; font-weight: 600; color: #94A3B8;">
        🏥 UAC System Capacity & Care Load Analytics
    </p>
    <p>Unified Mentor Project | Built with Streamlit, Prophet & Plotly</p>
    <p style="font-size: 0.8rem; color: #475569;">
        Data Source: U.S. Department of Health and Human Services | UAC Program
    </p>
</div>
""", unsafe_allow_html=True)
