🏥 UAC System Capacity & Care Load Analytics

Unaccompanied Children (UAC) Program | Real-Time Capacity Monitoring & Stress Detection
https://www.python.org/
https://streamlit.io/
https://facebook.github.io/prophet/
https://plotly.com/
LICENSE

🚀 Live Demo • 📊 Dashboard • 📄 Report
</div>


📖 Project Overview

The UAC System Capacity & Care Load Analytics is a data-driven decision support system developed to address the operational challenges within the U.S. 
Department of Health and Human Services (HHS) Unaccompanied Children (UAC) program.
As an AI & ML Engineer, I designed this solution to move beyond static reporting. 
By integrating statistical stress detection algorithms and advanced machine learning time-series forecasting (Prophet), 
the system provides stakeholders with the ability to visualize historical patterns, identify ongoing capacity backlogs, and predict future resource requirements before they reach critical levels.


🚀 Live Demo & Access

Experience the live application here:
🔗 Access the UAC System Analytics Dashboard
💡 Why This Project Matters
Managing unaccompanied children's care involves complex flow dynamics between border apprehension (CBP) and health services (HHS). 
This tool transforms raw, disparate data into actionable intelligence:
Predictive Capability: Forecasts capacity strain up to 365 days into the future.
Proactive Management: Identifies "Stress Periods" (periods where load exceeds rolling averages by 10%) to trigger early management interventions.
Data-Backed Reporting: Automates the creation of professional PDF executive summaries, saving hours of manual data processing.

🛠 Technical Architecture

This project is built using a modern AI/Data stack:
Frontend/UI: Streamlit for a highly responsive, user-centric dashboard.
Data Science: Pandas and NumPy for heavy-duty data cleaning, feature engineering, and metric calculation.
AI Forecasting: Prophet (by Meta) for robust time-series forecasting, incorporating seasonality (weekly/yearly) and specific policy-shift markers.
Visualization: Plotly for interactive, dynamic charts that allow users to filter, zoom, and explore data depths.
Document Automation: ReportLab for generating formal, professional PDF reports on demand.


📊 Key Features

Dynamic KPI Dashboard: Real-time visibility into Total System Load, Intake/Discharge rates, and Backlog accumulation.
AI-Powered Forecasting: Configurable forecast horizons with confidence intervals to help managers prepare for future trends.
Stress Detection Engine: Custom-built algorithms that monitor the difference between short-term (7-day) and long-term (14-day) rolling averages.
Historical Comparison: Built-in tools to compare two different periods, allowing for rapid impact analysis of policy changes or seasonal shifts.
Interactive Data Exploration: Deep-dive functionality allows for custom date-range filtering across all metrics.


⚙️ Installation & Setup

To run this project locally, ensure you have Python 3.9+ installed.
1. Clone the Repository:
bash
git clone [https://github.com/yunes-ai-eng/UAC-System-Capacity-and-Care-Load-Analytics.git
cd UAC-System-Capacity-and-Care-Load-Analytics](https://uac-system-capacity-and-care-load-analytics-bwudksut85gjiy3e2m.streamlit.app/)
2. Install Dependencies:
bash
pip install -r requirements.txt
3. Launch the Dashboard:
bash
streamlit run app.py


👨‍💻 Author

Eng. Yunes Abdulghani Mohammed Ghaleb
AI & ML Engineer
As a researcher and engineer specialized in AI and Machine Learning, I am passionate about leveraging technology to solve humanitarian and operational challenges.

📧 Email: alshameeri.ai.eng@gmail.com

🔗 LinkedIn: https://www.linkedin.com/in/yunes-abdulghani-mohammed-ghaleb-b854b02b1

🔗 GitHub: https://github.com/yunes-ai-eng

Project developed with focus on scalability, data integrity, and professional reporting standards.
