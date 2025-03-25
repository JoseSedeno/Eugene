# -------------------- PAGE CONFIG --------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px
import time

st.set_page_config(page_title="Eugene ROI Calculator", layout="wide")

# Custom CSS for styling
custom_css = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://raw.githubusercontent.com/JoseSedeno/Eugene/main/background.webp");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

h1, h2, h3, h4, h5, h6, .stMarkdown {
    color: #1C1363;
}

[data-testid="metric-container"] {
    background-color: #F2F3FF;
    border: 1px solid #DDD;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

button.stButton {
    background-color: #6E62C5;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
}

button.stButton:hover {
    background-color: #4E4A9C;
}

.st-expander {
    background-color: #F2F3FF;
    border-radius: 10px;
}

.stDataFrame {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

if "input_mode_selection" not in st.session_state:
    st.session_state["input_mode_selection"] = "Simplified"
if "user_type" not in st.session_state:
    st.session_state["user_type"] = "Doctor/Clinician"
if "results" not in st.session_state:
    st.session_state["results"] = {}




# -------------------- LOGO PLACEHOLDER --------------------

logo_base64 = "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"

def display_logo(logo_base64):
    if logo_base64.strip():
        img_html = f'<img src="data:image/png;base64,{logo_base64}" width="200">'
        st.markdown(img_html, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Logo not found. Please check your Base64 string.")

display_logo(logo_base64)

# -------------------- CONSTANTS --------------------

# ✅ Test Categories & Variants
TEST_TYPES = {
    "Core": {"base": "Core", "curly": "Core Complex Cases"},
    "Couples": {"base": "Couples", "curly": "Couples Complex Cases"},
    "Comprehensive": {"base": "Comprehensive", "curly": "Comprehensive Complex Cases"}
}

# ✅ Predefined Salary Assumptions for Simplified Mode (Annual Salary Divided by Hours Worked)
SIMPLIFIED_SALARY = {
    "GP": 180,                 # $180 per hour
    "OB/GYN": 220,             # $220 per hour
    "Fertility Specialist": 250 # $250 per hour
}

# ✅ Specialty-Based Medicare Billing Rates (MBS)
SPECIALTY_MBS = {
    "GP": {
        "Core": {"rate": 42.50}, "Core Complex Cases": {"rate": 85.00},
        "Couples": {"rate": 78.20}, "Couples Complex Cases": {"rate": 156.40},
        "Comprehensive": {"rate": 210.50}, "Comprehensive Complex Cases": {"rate": 421.00}
    },
    "OB/GYN": {
        "Core": {"rate": 85.20}, "Core Complex Cases": {"rate": 170.40},
        "Couples": {"rate": 120.75}, "Couples Complex Cases": {"rate": 241.50},
        "Comprehensive": {"rate": 250.00}, "Comprehensive Complex Cases": {"rate": 500.00}
    },
    "Fertility Specialist": {
        "Core": {"rate": 95.00}, "Core Complex Cases": {"rate": 190.00},
        "Couples": {"rate": 150.00}, "Couples Complex Cases": {"rate": 300.00},
        "Comprehensive": {"rate": 300.00}, "Comprehensive Complex Cases": {"rate": 600.00}
    }
}

# ✅ Updated Time Assumptions Per Test (Nurse time removed as tests are done from home)
SIMPLIFIED_TIME = {
    "Core": {"admin": 20, "nurse": 0, "doctor": 15, "research": 0},
    "Couples": {"admin": 25, "nurse": 0, "doctor": 30, "research": 30},
    "Comprehensive": {"admin": 30, "nurse": 0, "doctor": 45, "research": 60}
}

# ✅ Default Staff Costs for Simplified Mode
DEFAULT_STAFF_COSTS = {
    "admin_hourly": 45,   # $45/hour
    "nurse_hourly": 60,   # $60/hour
    "genetic_hourly": 90  # $90/hour
}

# ✅ Weekly Work Schedule (Used in Simplified Mode)
DEFAULT_WORK_SCHEDULE = {
    "doctors_per_clinic": 1,        # Start with at least 1 doctor
    "patients_per_hour": 4,         # Each doctor sees 4 patients per hour
    "working_hours_per_day": 8,     # 8-hour workday
    "days_per_week": 5              # 5 working days per week
}

# ✅ Logistics Costs (Only for Fertility Clinics)
LOGISTICS_COSTS = {
    "shipping": 500,          # Monthly shipping cost ($)
    "storage": 200,           # Monthly storage cost ($)
    "admin_logistics": 750,   # Admin logistics cost ($/month)
    "misc_logistics": 300     # Miscellaneous logistics ($/month)
}

# ✅ Genetic Counseling Private Market Hourly Cost
GENETIC_COUNSELING_PRIVATE_COST = 500  # $500/hour, confirmed from market research

# ✅ Probability of Complex Cases (based on references provided)
COMPLEX_CASE_PROBABILITIES = {
    "Core Complex Cases": 0.04,          # From Lynch et al., 2018 & Edwards et al., 2021
    "Couples Complex Cases": 0.06,       # Estimated higher due to complexity (assumption)
    "Comprehensive Complex Cases": 0.08  # Estimated higher due to complexity (assumption)
}


# -------------------- INPUT SECTIONS --------------------

def get_user_type():
    return st.radio(
        "Select your role:",
        ["Doctor/Clinician", "Owner/Manager"],
        horizontal=True,
        key="user_type",
        help="Choose whether you're an individual doctor/clinician or managing a clinic. This will affect staff and logistics inputs."
    )

def get_input_mode():
    return st.radio(
        "Choose Mode:",
        ["Simplified", "Advanced"],
        horizontal=True,
        key="input_mode_selection",
        help="Simplified mode uses predefined assumptions. Advanced mode allows full manual input of volumes and times."
    )

def get_practice_profile():
    with st.expander("🏥 Practice Profile", expanded=True):
        cols = st.columns(2)
        specialty = cols[0].selectbox(
            "Medical Specialty",
            list(SPECIALTY_MBS.keys()),
            key="specialty",
            help="Select the specialty of your practice. This determines MBS rates and doctor hourly cost assumptions."
        )

        operation_days = cols[1].slider(
            "Clinical Days/Week", 1, 7, 5,
            help="Number of days per week your clinic operates."
        )

        if st.session_state["input_mode_selection"] == "Advanced":
            weeks_year = st.slider(
                "Operational Weeks/Year", 40, 52, 48,
                help="Total weeks in the year that your clinic operates. Default is 48."
            )
        else:
            weeks_year = 48

        consults_per_hour = st.slider(
            "Patient Consults/Hour", 1, 6, 3,
            help="Average number of patient consultations per doctor, per hour."
        )

        return {
            "specialty": specialty,
            "operation_days": operation_days,
            "weeks_year": weeks_year,
            "consults_per_hour": consults_per_hour
        }

def get_staff_costs():
    with st.expander("💰 Staff Costs", expanded=True):
        cols = st.columns(2)
        specialty = st.session_state.get("specialty", "GP")

        if st.session_state["input_mode_selection"] == "Advanced":
            staff = {
                "num_admin": cols[0].number_input("Admin Staff", 1, 50, 1, help="Number of administrative staff employed."),
                "num_nurse": cols[1].number_input("Nurses", 1, 50, 1, help="Number of nurses in the clinic."),
                "num_doctor": cols[0].number_input("Doctors", 1, 50, 1, help="Number of doctors working in the clinic."),
                "num_genetic_counselor": cols[1].number_input("Genetic Counselors", 0, 50, 0, help="Number of in-house genetic counselors (if any)."),
                "admin_hourly": cols[0].number_input("Admin Hourly Rate ($)", 25, 100, 45, help="Hourly cost for administrative staff."),
                "nurse_hourly": cols[1].number_input("Nurse Hourly Rate ($)", 25, 100, 60, help="Hourly cost for nursing staff."),
                "doctor_hourly": cols[0].number_input("Doctor Hourly Rate ($)", 80, 300, 180, help="Hourly cost for doctors, based on specialty."),
                "genetic_hourly": cols[1].number_input("Genetic Counselor Hourly Rate ($)", 60, 200, 100, help="Hourly cost for genetic counseling staff.")
            }
        else:
            num_doctors = cols[0].number_input("Number of Doctors", 1, 50, 3, help="Total number of doctors in the clinic.") if st.session_state["user_type"] == "Owner/Manager" else 1

            staff = {
                "num_admin": 1,
                "num_nurse": 1,
                "num_doctor": num_doctors,
                "num_genetic_counselor": 0,
                "admin_hourly": DEFAULT_STAFF_COSTS["admin_hourly"],
                "nurse_hourly": DEFAULT_STAFF_COSTS["nurse_hourly"],
                "genetic_hourly": DEFAULT_STAFF_COSTS["genetic_hourly"],
                "doctor_hourly": SIMPLIFIED_SALARY.get(specialty, 180)
            }

        return staff

def get_logistical_costs():
    if st.session_state["user_type"] == "Owner/Manager" and st.session_state.get("specialty") == "Fertility Specialist":
        with st.expander("📦 Logistical Costs", expanded=True):
            cols = st.columns(2)
            return {
                "shipping": cols[0].number_input("Monthly Shipping Costs ($)", 0, 10000, 500, help="Shipping and transportation costs for tests and samples."),
                "storage": cols[1].number_input("Monthly Storage Costs ($)", 0, 5000, 200, help="Costs of storing samples or kits."),
                "admin_logistics": cols[0].number_input("Admin Logistics ($/month)", 0, 5000, 750, help="Administrative overhead costs related to logistics."),
                "misc_logistics": cols[1].number_input("Miscellaneous Logistics ($/month)", 0, 3000, 300, help="Any other logistics expenses.")
            }
    return {}

def get_billing_model():
    with st.expander("💵 Billing Model", expanded=True):
        model = st.radio(
            "Billing Type", ["Bulk Bill", "Mixed", "Private"], horizontal=True, key="billing_model",
            help="Select your clinic's billing method: Bulk Bill (standard rebates), Private billing, or a combination (Mixed)."
        )
        config = {"model": model}

        if model != "Bulk Bill":
            config["private_hourly"] = st.number_input(
                "Private Rate ($/hr)", 100, 800, 200,
                help="Your clinic's private billing hourly rate for consultations."
            )

        if model == "Mixed":
            bulk_rate = st.slider(
                "Bulk Bill Percentage (%)", 0, 100, 60,
                help="Percentage of patients billed via Bulk Bill. The rest will be billed privately."
            )
            config["bulk_rate"] = min(bulk_rate, 100)

        return config

def get_test_configuration(test_category):
    base = TEST_TYPES[test_category]["base"]
    curly = TEST_TYPES[test_category]["curly"]

    if st.session_state["input_mode_selection"] == "Simplified":
        with st.expander(f"🧬 {test_category} Testing"):
            base_weekly_volume = st.number_input(
                f"{base} Tests per Week", 0, 1000, 20, key=f"vol_{test_category}_base",
                help=f"Estimated number of {base.lower()} tests conducted each week."
            )

            complex_weekly_volume = base_weekly_volume * COMPLEX_CASE_PROBABILITIES.get(curly, 0.05)

            return {
                base: {
                    "weekly_volume": base_weekly_volume,
                    "admin_time": SIMPLIFIED_TIME[test_category]["admin"],
                    "nurse_time": SIMPLIFIED_TIME[test_category]["nurse"],
                    "doctor_time": SIMPLIFIED_TIME[test_category]["doctor"]
                },
                curly: {
                    "weekly_volume": complex_weekly_volume,
                    "research_time": SIMPLIFIED_TIME[test_category]["research"],
                    "genetic_time": 60
                }
            }
    else:
        with st.expander(f"🧬 {test_category} Testing"):
            return {
                base: {
                    "weekly_volume": st.number_input(f"{base} Tests per Week", 0, 1000, 20, key=f"vol_{test_category}_base", help=f"Number of {base.lower()} tests conducted each week."),
                    "admin_time": st.number_input("Admin Time (minutes per test)", 0, 240, 20, key=f"admin_{test_category}_base", help="Average admin processing time for each test."),
                    "nurse_time": st.number_input("Nurse Time (minutes per test)", 0, 240, 15, key=f"nurse_{test_category}_base", help="Nursing time involved per test (if any)."),
                    "doctor_time": st.number_input("Doctor Time (minutes per test)", 0, 240, 15, key=f"doctor_{test_category}_base", help="Doctor consultation time spent per test.")
                },
                curly: {
                    "weekly_volume": st.number_input("Complex Cases per Week", 0, 500, 1, key=f"vol_{test_category}_complex", help="Number of tests per week expected to result in complex findings."),
                    "research_time": st.number_input("Research Time (minutes per complex case)", 0, 480, 90, key=f"research_{test_category}_complex", help="Time the doctor spends researching complex cases."),
                    "genetic_time": st.number_input("Genetic Counseling Time (minutes per complex case)", 0, 360, 60, key=f"genetic_{test_category}_complex", help="Time spent in genetic counseling for each complex case.")
                }
            } 



# -------------------- CALCULATION FUNCTIONS --------------------

def calculate_annual_staff_costs(staff, test_config, weeks_year):
    """Calculates annual staff costs based on actual test workload rather than full-time hours."""
    try:
        total_cost = 0.0

        for test_type, test_variants in test_config.items():
            for variant, params in test_variants.items():
                if "weekly_volume" not in params:
                    continue

                annual_volume = params["weekly_volume"] * weeks_year

                admin_hours = (params.get("admin_time", 0) / 60) * annual_volume
                nurse_hours = (params.get("nurse_time", 0) / 60) * annual_volume
                doctor_hours = ((params.get("doctor_time", 0) + params.get("research_time", 0)) / 60) * annual_volume
                genetic_hours = (params.get("genetic_time", 0) / 60) * annual_volume

                total_cost += (
                    admin_hours * staff["admin_hourly"] +
                    nurse_hours * staff["nurse_hourly"] +
                    doctor_hours * staff["doctor_hourly"] +
                    genetic_hours * staff["genetic_hourly"]
                )

        return total_cost

    except Exception as e:
        st.error(f"Error in workload-based staff cost calculation: {str(e)}")
        return 0

def calculate_logistical_costs(logistics):
    """Calculates annual logistical costs for clinic owners (if applicable)."""
    try:
        return sum(logistics.values()) * 12 if logistics else 0  # Monthly to yearly conversion
    except Exception as e:
        st.error(f"Error in logistics calculation: {str(e)}")
        return 0

def calculate_efficiency_savings(test_config, staff, weeks_year):
    """Calculates efficiency savings and potential patient savings for complex cases."""
    savings = {}
    total_potential_patient_savings = 0.0

    simplified_mode = st.session_state.get("input_mode_selection", "Simplified") == "Simplified"

    for test_type, test_variants in test_config.items():
        for variant, params in test_variants.items():
            if "weekly_volume" not in params:
                continue

            annual_volume = params["weekly_volume"] * weeks_year

            time_components = {
                "admin": params.get("admin_time", 0) / 60,
                "nurse": params.get("nurse_time", 0) / 60,
                "doctor": (params.get("doctor_time", 0) + params.get("research_time", 0)) / 60,
                "genetic": params.get("genetic_time", 0) / 60
            }

            role_savings = {
                role: (time_components[role] * annual_volume * staff.get(f"{role}_hourly", 0))
                for role in ["admin", "nurse", "doctor", "genetic"]
            }

            if "Complex Cases" in variant:
                probability = COMPLEX_CASE_PROBABILITIES.get(variant, 0.05)
                if simplified_mode:
                    potential_patient_savings = (
                        time_components["genetic"] * annual_volume *
                        GENETIC_COUNSELING_PRIVATE_COST * probability
                    )
                else:
                    # In advanced mode, annual_volume = complex cases, no probability multiplier
                    potential_patient_savings = (
                        time_components["genetic"] * annual_volume *
                        GENETIC_COUNSELING_PRIVATE_COST
                    )
            else:
                potential_patient_savings = 0.0

            savings[f"{test_type} - {variant}"] = {
                "annual_volume": annual_volume,
                "total_savings": sum(role_savings.values()),
                "genetic_counselor_cost_avoided": potential_patient_savings,
                "time_breakdown": time_components
            }

            total_potential_patient_savings += potential_patient_savings

    return savings, total_potential_patient_savings


def calculate_revenue(test_configs, specialty, billing_model, practice):
    """Calculates total revenue based on billing model and MBS rates."""
    try:
        total_revenue = 0.0
        additional_revenue = 0.0
        total_doctor_hours_saved = 0.0

        for test_type, test_variants in test_configs.items():
            for variant, params in test_variants.items():
                if "weekly_volume" not in params:
                    continue

                annual_volume = params["weekly_volume"] * practice["weeks_year"]
                rate = SPECIALTY_MBS[specialty][variant]["rate"]
                doctor_hours = (params.get("doctor_time", 0) / 60) * annual_volume

                if billing_model["model"] == "Bulk Bill":
                    total_revenue += annual_volume * rate

                elif billing_model["model"] == "Private":
                    total_revenue += doctor_hours * billing_model["private_hourly"]

                else:  # Mixed model
                    bulk_volume = annual_volume * (billing_model["bulk_rate"] / 100)
                    private_volume = annual_volume - bulk_volume
                    total_revenue += (
                        bulk_volume * rate +
                        private_volume * billing_model["private_hourly"] * (params.get("doctor_time", 0) / 60)
                    )

                total_doctor_hours_saved += doctor_hours

        if billing_model["model"] != "Bulk Bill":
            additional_patients = total_doctor_hours_saved * practice["consults_per_hour"]
            additional_revenue = additional_patients * billing_model.get("private_hourly", 0)

        return total_revenue + additional_revenue, additional_revenue, total_doctor_hours_saved

    except Exception as e:
        st.error(f"Error in revenue calculation: {str(e)}")
        return 0, 0, 0

def run_calculations(practice, staff, billing, test_configs, logistics):
    """Runs all calculations and aggregates results."""
    results = {
        "total_annual_savings": 0.0,
        "total_revenue": 0.0,
        "additional_revenue": 0.0,
        "total_doctor_hours_saved": 0.0,
        "staff_costs": 0.0,
        "logistical_costs": 0.0,
        "net_annual_benefit": 0.0,
        "breakdown": {},
        "potential_patient_savings": 0.0,
        "total_staff_hours_saved": 0.0
    }

    try:
        results["staff_costs"] = calculate_annual_staff_costs(staff, test_configs, practice["weeks_year"])
        results["logistical_costs"] = calculate_logistical_costs(logistics)

        savings_data, total_patient_savings = calculate_efficiency_savings(
            test_configs, staff, practice["weeks_year"]
        )

        results["total_annual_savings"] = sum(v["total_savings"] for v in savings_data.values())
        results["potential_patient_savings"] = total_patient_savings
        results["breakdown"] = savings_data

        revenue_data = calculate_revenue(
            test_configs, practice["specialty"], billing, practice
        )

        results["total_revenue"] = revenue_data[0]
        results["additional_revenue"] = revenue_data[1]
        results["total_doctor_hours_saved"] = revenue_data[2]

        results["total_staff_hours_saved"] = sum(
            (data["time_breakdown"]["admin"] +
             data["time_breakdown"]["nurse"] +
             data["time_breakdown"]["doctor"] +
             data["time_breakdown"]["genetic"]) * data["annual_volume"]
            for data in savings_data.values()
        )

        results["net_annual_benefit"] = (
            results["total_annual_savings"] +
            results["total_revenue"] -
            results["staff_costs"] -
            results["logistical_costs"]
        )

    except Exception as e:
        st.error(f"Error in calculations: {str(e)}")

    if "Revenue Breakdown" not in results:
        results["Revenue Breakdown"] = pd.DataFrame()

    return results


# -------------------- EXPORT REPORT --------------------
def export_to_excel():
    if "results" not in st.session_state or not st.session_state["results"]:
        st.warning("⚠️ No results to export. Please run the calculation first.")
        return

    results = st.session_state["results"]

    # Check if revenue breakdown is present and not empty
    if "Revenue Breakdown" not in results or results["Revenue Breakdown"].empty:
        st.warning("⚠️ Revenue Breakdown is empty — please run the calculation again before exporting.")
        return

    show_logistics = (
        st.session_state["user_type"] == "Owner/Manager" and
        st.session_state.get("specialty") == "Fertility Specialist"
    )

    output = BytesIO()
    with st.spinner("Generating Excel report..."):
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            # Export revenue breakdown
            results["Revenue Breakdown"].to_excel(writer, sheet_name="Revenue Breakdown", index=False)

            # Export time and cost savings breakdown
            if "breakdown" in results:
                savings_data = []
                for test_type, data in results["breakdown"].items():
                    total_hours_saved = sum([
                        data["time_breakdown"][role] * data["annual_volume"]
                        for role in ["admin", "nurse", "doctor", "genetic"]
                    ])
                    savings_data.append({
                        'Test Type': test_type,
                        'Annual Volume': data["annual_volume"],
                        'Total Savings ($)': data["total_savings"],
                        'Admin Time Saved (hrs)': data["time_breakdown"]["admin"] * data["annual_volume"],
                        'Nurse Time Saved (hrs)': data["time_breakdown"]["nurse"] * data["annual_volume"],
                        'Doctor Time Saved (hrs)': data["time_breakdown"]["doctor"] * data["annual_volume"],
                        'Genetic Counselor Time Saved (hrs)': data["time_breakdown"]["genetic"] * data["annual_volume"],
                        'Total Staff Time Saved (hrs)': total_hours_saved
                    })
                df_savings = pd.DataFrame(savings_data)
                df_savings.to_excel(writer, sheet_name="Time & Cost Savings", index=False)

            # Export summary
            total_time_saved = sum(
                (data["time_breakdown"]["admin"] +
                 data["time_breakdown"]["nurse"] +
                 data["time_breakdown"]["doctor"] +
                 data["time_breakdown"]["genetic"]) * data["annual_volume"]
                for data in results["breakdown"].values()
            )

            summary_data = {
                "Total Revenue": [results["total_revenue"]],
                "Annual Savings": [results["total_annual_savings"]],
                "Potential Patient Savings": [results["potential_patient_savings"]],
                "Annual Doctor Time Saved (hrs)": [results["total_doctor_hours_saved"]],
                "Total Staff Time Saved (hrs)": [total_time_saved],
                "Workload-Based Staff Costs": [results["staff_costs"]]
            }

            if show_logistics:
                summary_data["Logistical Costs"] = [results["logistical_costs"]]

            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name="Summary", index=False)

            # Export patient savings data
            patient_savings_data = []
            for test_type, data in results["breakdown"].items():
                if "Complex Cases" in test_type and data["genetic_counselor_cost_avoided"] > 0:
                    variant_name = test_type.split(' - ')[-1]
                    probability = COMPLEX_CASE_PROBABILITIES.get(variant_name, 0.05)
                    patient_savings_data.append({
                        'Test Type': test_type,
                        'Annual Complex Volume': data["annual_volume"],
                        'Probability of Complex Finding': f"{probability * 100:.0f}%",
                        'Potential Patient Savings ($)': data["genetic_counselor_cost_avoided"]
                    })

            if patient_savings_data:
                df_patient_savings = pd.DataFrame(patient_savings_data)
                df_patient_savings.to_excel(writer, sheet_name="Patient Savings", index=False)

        output.seek(0)

    st.download_button(
        label="📥 Export Report to Excel",
        data=output,
        file_name="Eugene_ROI_Workload_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )



def show_before_after_animation(results):
    before_revenue = results['total_revenue'] - results['total_annual_savings']
    after_revenue = results['total_revenue']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=['Before Eugene'],
        y=[before_revenue],
        name='Before Eugene',
        marker_color='#1C1363',
        hovertemplate='Revenue before adopting Eugene.'
    ))

    fig.add_trace(go.Bar(
        x=['After Eugene'],
        y=[0],
        name='After Eugene',
        marker_color='#6E62C5',
        hovertemplate='Revenue after adopting Eugene.'
    ))

    fig.update_layout(
        title='Before vs. After Eugene: Revenue Impact',
        yaxis=dict(title='Annual Revenue ($)', tickformat=',.0f'),
        barmode='group',
        showlegend=False,
        plot_bgcolor='#F2F3FF',
        font=dict(color='#1C1363'),
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )

    plot_placeholder = st.empty()

    for i in range(1, 21):
        current_value = (after_revenue / 20) * i
        fig.data[1].y = [current_value]
        plot_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.05)


def main():
    st.title("Eugene ROI Calculator")

    debug_mode = st.sidebar.checkbox("🔎 Enable Debug Mode")

    if "results" not in st.session_state:
        st.session_state["results"] = {}

    col_input, col_output = st.columns([2, 3])

    with col_input:
        st.header("⚙️ Configure Inputs")

        user_type = st.radio("Select your role:", ["Doctor/Clinician", "Owner/Manager"], horizontal=True, key="user_type")
        input_mode = st.radio("Select Input Mode:", ["Simplified", "Advanced"], horizontal=True, key="input_mode_selection")

        practice = get_practice_profile()

        if user_type == "Owner/Manager":
            staff = get_staff_costs()
        else:
            specialty = st.session_state.get("specialty", "GP")
            staff = {
                "num_admin": 1,
                "num_nurse": 1,
                "num_doctor": 1,
                "admin_hourly": DEFAULT_STAFF_COSTS["admin_hourly"],
                "nurse_hourly": DEFAULT_STAFF_COSTS["nurse_hourly"],
                "genetic_hourly": DEFAULT_STAFF_COSTS["genetic_hourly"],
                "doctor_hourly": SIMPLIFIED_SALARY.get(specialty, 180)
            }

        logistics = get_logistical_costs() if user_type == "Owner/Manager" and st.session_state.get("specialty") == "Fertility Specialist" else {}

        billing = get_billing_model()

        st.subheader("🧬 Test Configuration")
        test_configs = {
            "Core": get_test_configuration("Core"),
            "Couples": get_test_configuration("Couples"),
            "Comprehensive": get_test_configuration("Comprehensive")
        }

        if debug_mode:
            st.subheader("🔎 Debug Information")
            st.write("Practice Profile:", practice)
            st.write("Staff Config:", staff)
            st.write("Billing Model:", billing)
            st.write("Test Configurations:", test_configs)

            specialty = practice["specialty"]
            st.write(f"Checking MBS keys for specialty: {specialty}")
            for test_type, test_variants in test_configs.items():
                for variant in test_variants.keys():
                    if variant not in SPECIALTY_MBS[specialty]:
                        st.warning(f"⚠️ Variant '{variant}' is missing in MBS rates for {specialty}.")

        calculate = st.button("📊 Calculate ROI")

    with col_output:
        if calculate:
            with st.spinner("Calculating ROI..."):
                results = run_calculations(practice, staff, billing, test_configs, logistics)
                st.session_state["results"] = results
            st.success("✅ ROI calculation completed successfully!")

            revenue_data = []
            for test_type, test_variants in test_configs.items():
                for variant, params in test_variants.items():
                    try:
                        if variant not in SPECIALTY_MBS[practice["specialty"]]:
                            st.warning(f"⚠️ Skipping '{variant}' as it’s not defined in MBS rates for {practice['specialty']}")
                            continue

                        rate = SPECIALTY_MBS[practice["specialty"]][variant]["rate"]
                        revenue = params["weekly_volume"] * practice["weeks_year"] * rate
                        revenue_data.append({"Test Type": f"{test_type} - {variant}", "Revenue": revenue})
                    except Exception as e:
                        st.error(f"Error calculating revenue for '{variant}': {e}")

            df_revenue = pd.DataFrame(revenue_data)
            st.session_state["results"]["Revenue Breakdown"] = df_revenue

            st.header("📈 Financial Summary")
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Staff Costs", f"${results['staff_costs']:,.0f}", help="Total annual staff costs based on actual workload.")
            col2.metric("Total Revenue", f"${results['total_revenue']:,.0f}", help="Total revenue from tests, based on billing model and doctor time.")
            col3.metric("Annual Efficiency Savings", f"${results['total_annual_savings']:,.0f}", help="Annual time and efficiency savings from using Eugene.")
            col4.metric("Net Annual Benefit", f"${results['net_annual_benefit']:,.0f}", help="Revenue plus savings minus staff and logistics costs.")

            st.subheader("💡 Patient Benefits")
            col_patient1, col_patient2 = st.columns([1, 3])
            col_patient1.metric("Potential Patient Savings", f"${results['potential_patient_savings']:,.0f}", help="Money patients save by using Eugene, which includes genetic counseling for complex cases (valued at $500/hour).")
            col_patient2.write("**Using Eugene avoids an estimated 6-month public health wait time and includes genetic counseling at no extra cost.**")

            with st.expander("🔎 Patient Savings Breakdown (Complex Cases)"):
                st.caption("Estimated complex case volumes and the value of included counseling savings.")
                patient_savings_data = []
                for test_type, data in results["breakdown"].items():
                    if "Complex Cases" in test_type and data["genetic_counselor_cost_avoided"] > 0:
                        variant_name = test_type.split(' - ')[-1]
                        probability = COMPLEX_CASE_PROBABILITIES.get(variant_name, 0.05)
                        patient_savings_data.append({
                            'Test Type': test_type,
                            'Annual Complex Volume': data["annual_volume"],
                            'Probability of Complex Finding': f"{probability * 100:.0f}%" if input_mode == "Simplified" else "Manual Entry",
                            'Potential Savings ($)': data["genetic_counselor_cost_avoided"]
                        })
                if patient_savings_data:
                    df_patient_savings = pd.DataFrame(patient_savings_data)
                    st.dataframe(df_patient_savings.style.format({'Potential Savings ($)': '${:,.0f}'}))

            st.subheader("Eugene’s Impact: Savings and Revenue Opportunities")

            categories = ["Annual Efficiency Savings", "Potential Additional Revenue"]
            amounts = [
                results["total_annual_savings"],
                results["total_revenue"]
            ]

            explanations = [
                "Time and efficiency savings generated by using Eugene.",
                "Additional revenue opportunities unlocked for your clinic."
            ]

            if user_type == "Owner/Manager" and st.session_state.get("specialty") == "Fertility Specialist":
                categories.append("Logistics Costs")
                amounts.append(results["logistical_costs"])
                explanations.append("Annual clinic logistics expenses.")

            overview_data = {"Category": categories, "Amount": amounts, "Explanation": explanations}

            fig = px.bar(
                overview_data,
                x='Category',
                y='Amount',
                color='Category',
                text='Amount',
                hover_data={'Explanation': True, 'Amount': False, 'Category': False},
                color_discrete_map={
                    'Annual Efficiency Savings': '#00C853',
                    'Potential Additional Revenue': '#1C1363',
                    'Logistics Costs': '#FF8C00'
                }
            )

            fig.update_traces(
                texttemplate='%{text:$.0f}',
                textposition='outside',
                hovertemplate='%{customdata[0]}'
            )

            fig.update_layout(
                title='Eugene’s Impact: Savings and Revenue Opportunities',
                xaxis=dict(title='Category'),
                yaxis=dict(title='Amount', tickformat=',.0f'),
                showlegend=False,
                xaxis_showgrid=False,
                yaxis_showgrid=False
            )

            st.plotly_chart(fig, use_container_width=True)

            show_before_after_animation(results)

            with st.expander("📊 Revenue Breakdown"):
                st.caption("Revenue by test type based on Medicare and private billing.")
                st.dataframe(df_revenue.style.format({'Revenue': '${:,.0f}'}))

            with st.expander("⏳ Time & Cost Savings Breakdown"):
                savings_data = []
                for test_type, data in results["breakdown"].items():
                    savings_data.append({
                        'Test Type': test_type,
                        'Annual Volume': data["annual_volume"],
                        'Total Savings ($)': data["total_savings"],
                        'Admin Time Saved (hrs)': data["time_breakdown"]["admin"] * data["annual_volume"],
                        'Nurse Time Saved (hrs)': data["time_breakdown"]["nurse"] * data["annual_volume"],
                        'Doctor Time Saved (hrs)': data["time_breakdown"]["doctor"] * data["annual_volume"],
                        'Genetic Counselor Time Saved (hrs)': data["time_breakdown"]["genetic"] * data["annual_volume"]
                    })
                df_savings = pd.DataFrame(savings_data)
                st.dataframe(df_savings.style.format({'Total Savings ($)': '${:,.0f}'}))

    st.subheader("⬇️ Download Report")
    if st.button("📥 Export Full Financial Report"):
        export_to_excel()
        st.success("✅ Excel report generated and ready for download!")


if __name__ == "__main__":
    main()
