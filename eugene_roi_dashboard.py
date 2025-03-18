# -------------------- PAGE CONFIG --------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from io import BytesIO

# ✅ Set Streamlit page configuration
st.set_page_config(page_title="Eugene ROI Calculator", layout="wide")

# ✅ Initialize session state defaults
if "input_mode_selection" not in st.session_state:
    st.session_state["input_mode_selection"] = "Simplified"

if "user_type" not in st.session_state:
    st.session_state["user_type"] = "Doctor/Clinician"

if "results" not in st.session_state:
    st.session_state["results"] = {}


# -------------------- LOGO PLACEHOLDER --------------------

logo_base64 = """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"""

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

# ✅ Predefined Salary Assumptions for Simplified Mode
SIMPLIFIED_SALARY = {
    "GP": 180,  
    "OB/GYN": 220,  
    "Fertility Specialist": 250  
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

# ✅ Default Staff Costs for Simplified Mode
DEFAULT_STAFF_COSTS = {
    "admin_hourly": 45,  
    "nurse_hourly": 60,  
    "genetic_hourly": 90  
}

# ✅ Time Assumptions per Test (used in Simplified Mode)
SIMPLIFIED_TIME = {
    "Core": {"admin": 20, "nurse": 15, "doctor": 15, "research": 0},
    "Couples": {"admin": 25, "nurse": 20, "doctor": 30, "research": 30},
    "Comprehensive": {"admin": 30, "nurse": 20, "doctor": 45, "research": 60}
}

# ✅ Weekly Work Schedule Defaults (for simplified mode logic if needed)
DEFAULT_WORK_SCHEDULE = {
    "doctors_per_clinic": 1,
    "patients_per_hour": 4,
    "working_hours_per_day": 8,
    "days_per_week": 5
}

# ✅ Logistics costs (optional for fertility clinic owners)
LOGISTICS_COSTS = {
    "shipping": 500,  
    "storage": 200,  
    "admin_logistics": 750,  
    "misc_logistics": 300  
}

# -------------------- INPUT SECTIONS --------------------

def get_user_type():
    """Ensures session state is initialized & user selects role."""
    if "user_type" not in st.session_state:
        st.session_state["user_type"] = "Doctor/Clinician"  # Default selection

    return st.radio(
        "Select your role:",
        ["Doctor/Clinician", "Owner/Manager"],
        horizontal=True,
        key="user_type"
    )

def get_input_mode():
    """Allows user to select Simplified or Advanced mode."""
    if "input_mode_selection" not in st.session_state:
        st.session_state["input_mode_selection"] = "Simplified"  # Default mode

    return st.radio(
        "Choose Mode:",
        ["Simplified", "Advanced"],
        horizontal=True,
        key="input_mode_selection"
    )

def get_practice_profile():
    """Collects practice details dynamically."""
    with st.expander("🏥 Practice Profile", expanded=True):
        cols = st.columns(2)
        specialty = cols[0].selectbox(
            "Medical Specialty",
            list(SPECIALTY_MBS.keys()),
            key="specialty"  # Streamlit will manage this in session state
        )

        practice = {
            "specialty": specialty,
            "operation_days": cols[1].slider("Clinical Days/Week", 1, 7, 5),
            "weeks_year": st.slider("Operational Weeks/Year", 40, 52, 46),
            "consults_per_hour": st.slider("Patient Consults/Hour", 1, 6, 3)
        }

        if st.session_state["user_type"] == "Owner/Manager":
            practice["num_doctors"] = st.number_input("Number of Doctors", 1, 50, 3)

        return practice

def get_staff_costs():
    """Collects staff costs dynamically and ensures fallback for Simplified mode."""
    with st.expander("💰 Staff Costs", expanded=True):
        cols = st.columns(2)
        specialty = st.session_state.get("specialty", "GP")  # Default fallback

        staff = {
            "num_admin": cols[0].number_input("Admin Staff", 1, 50, 3),
            "num_nurse": cols[1].number_input("Nurses", 1, 50, 2),
            "num_doctor": cols[0].number_input("Doctors", 1, 50, 1),
            "num_genetic_counselor": cols[1].number_input("Genetic Counselors", 0, 50, 1),
        }

        if st.session_state["input_mode_selection"] == "Advanced":
            staff["admin_hourly"] = cols[0].number_input("Admin Hourly ($)", 25, 100, 45)
            staff["nurse_hourly"] = cols[1].number_input("Nurse Hourly ($)", 25, 100, 60)
            staff["doctor_hourly"] = cols[0].number_input("Doctor Hourly ($)", 80, 300, 150)
            staff["genetic_hourly"] = cols[1].number_input("Genetic Counselor Hourly ($)", 60, 200, 90)
        else:
            staff["admin_hourly"] = DEFAULT_STAFF_COSTS["admin_hourly"]
            staff["nurse_hourly"] = DEFAULT_STAFF_COSTS["nurse_hourly"]
            staff["genetic_hourly"] = DEFAULT_STAFF_COSTS["genetic_hourly"]
            staff["doctor_hourly"] = SIMPLIFIED_SALARY.get(specialty, 180)

        return staff

def get_logistical_costs():
    """Collects logistical costs (only if Fertility Specialist owner)."""
    if st.session_state["user_type"] == "Owner/Manager" and st.session_state.get("specialty") == "Fertility Specialist":
        with st.expander("📦 Logistical Costs", expanded=True):
            cols = st.columns(2)
            return {
                "shipping": cols[0].number_input("Monthly Shipping Costs ($)", 0, 10000, 500),
                "storage": cols[1].number_input("Monthly Storage Costs ($)", 0, 5000, 200),
                "admin_logistics": cols[0].number_input("Administrative Logistics ($/month)", 0, 3000, 750),
                "misc_logistics": cols[1].number_input("Miscellaneous Logistics ($/month)", 0, 2000, 300)
            }
    return {}

def get_billing_model():
    """Collects billing model with validation."""
    with st.expander("💵 Billing Model", expanded=True):
        model = st.radio("Billing Type", ["Bulk Bill", "Mixed", "Private"], horizontal=True, key="billing_model")
        config = {"model": model}

        if model != "Bulk Bill":
            config["private_hourly"] = st.number_input("Private Rate ($/hr)", 100, 500, 200)

        if model == "Mixed":
            bulk_rate = st.slider("Bulk Percentage", 0, 100, 60)
            config["bulk_rate"] = min(bulk_rate, 100)

        return config

def get_test_configuration(test_category):
    """Collects test parameters dynamically based on mode."""
    base = TEST_TYPES[test_category]["base"]
    curly = TEST_TYPES[test_category]["curly"]
    input_mode = st.session_state.get("input_mode_selection", "Simplified")

    with st.expander(f"🧬 {test_category} Testing"):
        weekly_volume = st.number_input(f"{base} Tests/Week", 0, 1000, 20, key=f"vol_{test_category}_base")
        complex_cases = st.number_input("Complex Cases/Week", 0, 500, 10, key=f"vol_{test_category}_complex")

        if input_mode == "Advanced":
            return {
                base: {
                    "weekly_volume": weekly_volume,
                    "admin_time": st.number_input("Admin Time (mins)", 0, 240, 20, key=f"admin_{test_category}_base"),
                    "nurse_time": st.number_input("Nurse Time (mins)", 0, 240, 15, key=f"nurse_{test_category}_base"),
                    "doctor_time": st.number_input("Doctor Time (mins)", 0, 240, 15, key=f"doctor_{test_category}_base"),
                },
                curly: {
                    "weekly_volume": complex_cases,
                    "research_time": st.number_input("Research Time (mins)", 0, 480, 90, key=f"research_{test_category}_complex"),
                    "genetic_time": st.number_input("Genetic Counseling (mins)", 0, 360, 60, key=f"genetic_{test_category}_complex"),
                }
            }
        else:
            return {
                base: {
                    "weekly_volume": weekly_volume,
                    "admin_time": SIMPLIFIED_TIME[test_category]["admin"],
                    "nurse_time": SIMPLIFIED_TIME[test_category]["nurse"],
                    "doctor_time": SIMPLIFIED_TIME[test_category]["doctor"],
                },
                curly: {
                    "weekly_volume": complex_cases,
                    "research_time": SIMPLIFIED_TIME[test_category]["research"],
                    "genetic_time": 60,  # Based on literature
                }
            }

# -------------------- CALCULATION FUNCTIONS --------------------

def calculate_annual_staff_costs(staff, practice):
    """Calculates total annual staff costs."""
    try:
        weekly_hours = practice["operation_days"] * 8  # Assuming 8-hour days
        annual_hours = weekly_hours * practice["weeks_year"]

        return sum([
            staff["num_admin"] * staff["admin_hourly"] * annual_hours,
            staff["num_nurse"] * staff["nurse_hourly"] * annual_hours,
            staff["num_doctor"] * staff["doctor_hourly"] * annual_hours,
            staff.get("num_genetic_counselor", 0) * staff.get("genetic_hourly", 0) * annual_hours
        ])
    except Exception as e:
        st.error(f"Error in staff cost calculation: {str(e)}")
        return 0

def calculate_logistical_costs(logistics):
    """Converts monthly logistics costs to annual totals."""
    try:
        return sum(logistics.values()) * 12 if logistics else 0
    except Exception as e:
        st.error(f"Error in logistics calculation: {str(e)}")
        return 0

def calculate_efficiency_savings(test_config, staff, weeks_year):
    """Computes time and cost savings across roles and test types."""
    savings = {}

    try:
        for test_type, variants in test_config.items():
            for variant, params in variants.items():
                if "weekly_volume" not in params:
                    continue  

                annual_volume = params["weekly_volume"] * weeks_year

                time_breakdown = {
                    "admin": params.get("admin_time", 0) / 60,
                    "nurse": params.get("nurse_time", 0) / 60,
                    "doctor": (params.get("doctor_time", 0) + params.get("research_time", 0)) / 60,
                    "genetic": params.get("genetic_time", 0) / 60
                }

                role_savings = {
                    role: (time_breakdown[role] * annual_volume * staff[f"{role}_hourly"])
                    for role in ["admin", "nurse", "doctor", "genetic"]
                    if f"{role}_hourly" in staff
                }

                savings[f"{test_type} - {variant}"] = {
                    "annual_volume": annual_volume,
                    "total_savings": sum(role_savings.values()),
                    "time_breakdown": time_breakdown
                }
        return savings
    except Exception as e:
        st.error(f"Error in efficiency savings calculation: {str(e)}")
        return {}

def calculate_revenue(test_configs, specialty, billing_model, practice):
    """Calculates revenue, additional revenue from freed doctor hours, and hours saved."""
    try:
        total_revenue = 0.0
        additional_revenue = 0.0
        total_doctor_hours_saved = 0.0

        for test_type, variants in test_configs.items():
            for variant, params in variants.items():
                if "weekly_volume" not in params:
                    continue  

                annual_volume = params["weekly_volume"] * practice["weeks_year"]
                rate = SPECIALTY_MBS[specialty][test_type]["rate"]
                doctor_hours = (params.get("doctor_time", 0) / 60) * annual_volume

                if billing_model["model"] == "Bulk Bill":
                    total_revenue += annual_volume * rate
                elif billing_model["model"] == "Private":
                    total_revenue += doctor_hours * billing_model["private_hourly"]
                else:
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
    """Runs all calculations and aggregates final results."""
    results = {
        "total_annual_savings": 0.0,
        "total_revenue": 0.0,
        "additional_revenue": 0.0,
        "total_doctor_hours_saved": 0.0,
        "staff_costs": 0.0,
        "logistical_costs": 0.0,
        "net_annual_benefit": 0.0,
        "breakdown": {}
    }

    try:
        results["staff_costs"] = calculate_annual_staff_costs(staff, practice)
        results["logistical_costs"] = calculate_logistical_costs(logistics)
        savings_data = calculate_efficiency_savings(test_configs, staff, practice["weeks_year"])

        results["total_annual_savings"] = sum(v["total_savings"] for v in savings_data.values())
        results["breakdown"] = savings_data

        revenue_data = calculate_revenue(test_configs, practice["specialty"], billing, practice)
        results["total_revenue"] = revenue_data[0]
        results["additional_revenue"] = revenue_data[1]
        results["total_doctor_hours_saved"] = revenue_data[2]

        results["net_annual_benefit"] = (
            results["total_annual_savings"] +
            results["total_revenue"] -
            results["staff_costs"] -
            results["logistical_costs"]
        )
    except Exception as e:
        st.error(f"Error in run calculations: {str(e)}")

    return results


# -------------------- MAIN APP LAYOUT --------------------

def main():
    st.title("Eugene ROI Calculator")

    # ✅ Ensure results state exists
    if "results" not in st.session_state:
        st.session_state["results"] = {}

    col_input, col_output = st.columns([2, 3])

    with col_input:
        st.header("⚙️ Configure Inputs")

        # ✅ Important fix: use the same session_state key for user_type
        user_type = st.radio("Select your role:", ["Doctor/Clinician", "Owner/Manager"], horizontal=True, key="user_type")
        input_mode = st.radio("Select Input Mode:", ["Simplified", "Advanced"], horizontal=True, key="input_mode_selection")

        practice = get_practice_profile()

        if user_type == "Owner/Manager":
            staff = get_staff_costs()
        else:
            # Doctor/Clinician default setup
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

        logistics = get_logistical_costs() if user_type == "Owner/Manager" else {}
        billing = get_billing_model()

        st.subheader("🧬 Test Configuration")
        test_configs = {
            "Core": get_test_configuration("Core"),
            "Couples": get_test_configuration("Couples"),
            "Comprehensive": get_test_configuration("Comprehensive")
        }

        calculate = st.button("📊 Calculate ROI")

    with col_output:
        if calculate:
            results = run_calculations(practice, staff, billing, test_configs, logistics)
            st.session_state["results"] = results

            revenue_data = []
            for test_type, test_variants in test_configs.items():
                for variant, params in test_variants.items():
                    rate = SPECIALTY_MBS[practice["specialty"]][test_type]["rate"]
                    revenue = params["weekly_volume"] * practice["weeks_year"] * rate
                    revenue_data.append({"Test Type": f"{test_type} - {variant}", "Revenue": revenue})

            df_revenue = pd.DataFrame(revenue_data)
            st.session_state["results"]["Revenue Breakdown"] = df_revenue

            st.header("📈 Financial Summary")
            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric("Staff Costs", f"${results['staff_costs']:,.0f}")
            col2.metric("Logistical Costs", f"${results['logistical_costs']:,.0f}")
            col3.metric("Total Revenue", f"${results['total_revenue']:,.0f}")
            col4.metric("Annual Savings", f"${results['total_annual_savings']:,.0f}")
            col5.metric("Net Benefit", f"${results['net_annual_benefit']:,.0f}",
                        delta_color="inverse" if results['net_annual_benefit'] < 0 else "normal")

            st.subheader("Annual Financial Overview")
            fig, ax = plt.subplots(figsize=(8, 4))
            categories = ['Staff Costs', 'Logistics', 'Revenue', 'Savings', 'Net']
            values = [
                results["staff_costs"],
                results["logistical_costs"],
                results["total_revenue"],
                results["total_annual_savings"],
                results["net_annual_benefit"]
            ]
            colors = ['#FF4B4B', '#FF4B4B', '#00C853', '#00C853',
                      '#FF4B4B' if results["net_annual_benefit"] < 0 else '#00C853']

            ax.bar(categories, values, color=colors)
            ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
            plt.xticks(rotation=45)
            st.pyplot(fig)

            with st.expander("📊 Revenue Breakdown"):
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
                        'Genetic Counselor Time Saved (hrs)': data["time_breakdown"]["genetic"] * data["annual_volume"],
                    })
                df_savings = pd.DataFrame(savings_data)
                st.dataframe(df_savings.style.format({'Total Savings ($)': '${:,.0f}'}))

if __name__ == "__main__":
    main()


# -------------------- EXPORT REPORT --------------------

def export_to_excel():
    """Exports results as an Excel file."""
    if "results" not in st.session_state or not st.session_state["results"]:
        st.warning("⚠️ No results to export. Please run the calculation first.")
        return

    results = st.session_state["results"]

    if "Revenue Breakdown" not in results:
        st.error("🚨 Missing Revenue Breakdown! Please re-run calculations.")
        return

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Export Revenue Breakdown
        results["Revenue Breakdown"].to_excel(writer, sheet_name="Revenue Breakdown", index=False)

        # Export Time & Cost Savings Breakdown
        if "breakdown" in results:
            savings_data = []
            for test_type, data in results["breakdown"].items():
                savings_data.append({
                    'Test Type': test_type,
                    'Annual Volume': data["annual_volume"],
                    'Total Savings ($)': data["total_savings"],
                    'Admin Time Saved (hrs)': data["time_breakdown"]["admin"] * data["annual_volume"],
                    'Nurse Time Saved (hrs)': data["time_breakdown"]["nurse"] * data["annual_volume"],
                    'Doctor Time Saved (hrs)': data["time_breakdown"]["doctor"] * data["annual_volume"],
                    'Genetic Counselor Time Saved (hrs)': data["time_breakdown"]["genetic"] * data["annual_volume"],
                })
            df_savings = pd.DataFrame(savings_data)
            df_savings.to_excel(writer, sheet_name="Time & Cost Savings", index=False)

        # Export Summary Metrics
        summary_data = {
            "Staff Costs": [results["staff_costs"]],
            "Logistical Costs": [results["logistical_costs"]],
            "Total Revenue": [results["total_revenue"]],
            "Annual Savings": [results["total_annual_savings"]],
            "Net Benefit": [results["net_annual_benefit"]]
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name="Summary", index=False)

    output.seek(0)

    st.download_button(
        label="📥 Export Report to Excel",
        data=output,
        file_name="Eugene_ROI_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ✅ Display export option only after calculation
st.header("📤 Export Report")
st.button("📥 Generate & Export Report", on_click=export_to_excel)
