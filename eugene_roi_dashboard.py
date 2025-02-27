import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from openpyxl import Workbook

# -------------------- MUST BE FIRST: PAGE CONFIG --------------------
st.set_page_config(page_title="Eugene ROI Calculator", layout="wide")

# -------------------- LOGO SUPPORT --------------------
# Paste your Base64 logo string inside the triple quotes below
base64_logo = """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"""

# Display the logo at the top of the app
if base64_logo:
    st.markdown(f'<img src="data:image/png;base64,{base64_logo}" width="200">', unsafe_allow_html=True)

# Initialize columns
left_col, right_col = st.columns([0.4, 0.6])

# -------------------- LEFT COLUMN: INPUTS --------------------
with left_col:
    st.header("⚙️ Practice Configuration")
    
    with st.expander("🏥 Clinic Profile", expanded=True):
        doctor_type = st.selectbox("Specialty", ["GP", "OB/GYN", "Fertility Specialist"])
        operation_days = st.slider("Clinical Days/Week", 1, 7, 5)
        weeks_year = st.slider("Operational Weeks/Year", 40, 52, 48)
        admin_hourly = st.number_input("Admin Hourly Rate ($)", 25, 100, 45, key="admin_hourly")
        nurse_hourly = st.number_input("Nurse Hourly Rate ($)", 25, 100, 45, key="nurse_hourly")
    
    with st.expander("🧪 Test Configuration", expanded=True):
        st.subheader("Test Type Allocation (%)")
        col1, col2 = st.columns(2)
        with col1:
            couples_test = st.slider("Couples Test %", 0, 100, 50)
        with col2:
            core_test = st.slider("Core Test %", 0, 100, 30)
            comprehensive_test = st.slider("Comprehensive Test %", 0, 100, 20)

    with st.expander("🩺 Clinical Workflow"):
        st.subheader("Admin & Nurse Costs Per Hour")
        col1, col2 = st.columns(2)
        with col1:
            admin_cost_hour = st.number_input("Admin Cost Per Hour ($)", 20, 100, 45, key="admin_cost_hour")
        with col2:
            nurse_salary_hour = st.number_input("Nurse Salary Per Hour ($)", 25, 150, 60, key="nurse_salary_hour")
        
        st.subheader("Admin & Nurse Time Allocation (mins)")
        col3, col4 = st.columns(2)
        with col3:
            admin_time = st.number_input("Admin Time (mins)", 5, 60, 20, key="admin_time")
        with col4:
            nurse_time = st.number_input("Nurse Time (mins)", 5, 60, 20, key="nurse_time")

        risk_level = st.selectbox("Risk Level", ["Low", "High"])

    with st.expander("🧬 Genetic Testing"):
        test_types = st.selectbox("Test Type", ["Core", "Couples", "Comprehensive"])
        st.subheader("Overall Test Time (mins, including follow-ups)")
        overall_test_time = st.number_input("Total Test Time", 30, 180, 60)
        
    with st.expander("💵 Financial Model"):
        billing_model = st.radio("Billing Type", ["Bulk Bill", "Mixed", "Private"], horizontal=True)
        if billing_model != "Bulk Bill":
            gap_fee = st.number_input("Patient Gap Fee ($)", 50, 300, 120)
        if billing_model == "Mixed":
            bulk_rate = st.slider("Bulk Billing %", 0, 100, 60)

# -------------------- RIGHT COLUMN: RESULTS --------------------
with right_col:
    st.header("📊 Impact Analysis")
    
    # -------------------- CALCULATIONS --------------------
    annual_patients = operation_days * weeks_year * 20  # Assume 20 patients per day
    total_time_saved = ((admin_time + nurse_time) * 0.3 * annual_patients) / 60
    revenue_gain = (annual_patients * 0.3 * (gap_fee if billing_model == "Private" else 120)) + ((admin_hourly + nurse_hourly) / 2 * 1.5 * weeks_year * operation_days)
    capacity_increase = (total_time_saved * 60) / overall_test_time

    # Key Metrics
    cols = st.columns(3)
    cols[0].metric("Annual Time Saved", f"{total_time_saved:,.1f} hrs")
    cols[1].metric("Revenue Potential", f"${revenue_gain:,.0f}")
    cols[2].metric("Capacity Increase", f"{capacity_increase:,.0f} pts")

    # Visualizations
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))

    # Time Allocation Breakdown
    time_data = {'Couples': couples_test, 'Core': core_test, 'Comprehensive': comprehensive_test}
    ax[0].pie(time_data.values(), labels=time_data.keys(), autopct='%1.1f%%')
    ax[0].set_title("Test Type Distribution")

    # Financial Impact
    financial_data = {'Patient Revenue': revenue_gain * 0.7, 'Staff Savings': revenue_gain * 0.3}
    ax[1].bar(financial_data.keys(), financial_data.values(), color=['#4B88E2', '#28C76F'])
    ax[1].set_title("Revenue Composition")

    st.pyplot(fig)

    # Detailed Report
    with st.expander("📄 Detailed Breakdown"):
        report_data = {'Metric': ['Total Clinical Hours Saved', 'Staff Cost Savings', 'Administrative Efficiency', 'Patient Throughput'],
                       'Value': [total_time_saved, ((admin_hourly + nurse_hourly) / 2 * 1.5 * weeks_year * operation_days), '35% Improvement', f"+{capacity_increase:,.0f} patients"]}
        st.dataframe(pd.DataFrame(report_data), hide_index=True)

    # Excel Export
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer) as writer:
        pd.DataFrame([time_data]).to_excel(writer, sheet_name='Time Analysis')
        pd.DataFrame([financial_data]).to_excel(writer, sheet_name='Financials')
    
    st.download_button(
        label="📥 Download Full Report",
        data=excel_buffer.getvalue(),
        file_name="eugene_detailed_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# -------------------- END --------------------
