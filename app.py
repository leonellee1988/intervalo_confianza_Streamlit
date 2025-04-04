import streamlit as st
from scipy.stats import norm, t

# App Title
st.title("Confidence Interval (CI) Calculator")

# Sidebar for Segmenters
with st.sidebar:
    # Segment: Calculation Type
    calculation_type = st.selectbox(
        "What would you like to calculate?",
        ["", "Mean", "Proportion"]  # Default blank value
    )

    # Segment: Sample Size (if applicable)
    sample_size_type = None
    if calculation_type == "Mean":
        sample_size_type = st.selectbox(
            "What is your sample size?",
            ["", "Large (≥ 30)", "Small (< 30)"]  # Default blank value
        )

# Main Section for Inputs
sample_mean_or_proportion = st.number_input(
    "Enter the sample mean or proportion:",
    format="%.4f",
    value=0.0  # Initial value set to 0.0
)

significance_level = st.selectbox(
    "Select the significance level (α):",
    ["", 0.10, 0.05, 0.01]  # Default blank value
)

standard_deviation = None
if calculation_type == "Mean":
    standard_deviation = st.number_input(
        "Enter the standard deviation:",
        format="%.4f",
        value=0.0  # Initial value set to 0.0
    )

sample_size = st.number_input(
    "Enter the sample size:",
    format="%d",
    min_value=1
)

# Validation: Large sample must be ≥ 30
if sample_size_type == "Large (≥ 30)" and sample_size < 30:
    st.error("Sample size must be at least 30 for large samples.")

# Button to Calculate
if st.button("Calculate"):
    if not calculation_type or not sample_mean_or_proportion or not significance_level or \
       (calculation_type == "Mean" and not standard_deviation) or not sample_size or \
       (calculation_type == "Mean" and not sample_size_type):
        st.error("Please complete all required information.")
    else:
        # Confidence Interval Calculation
        if calculation_type == "Mean":
            if sample_size_type == "Large (≥ 30)":
                z_value = norm.ppf(1 - significance_level / 2)
                margin_of_error = z_value * (standard_deviation / (sample_size ** 0.5))
            else:
                t_value = t.ppf(1 - significance_level / 2, df=sample_size - 1)
                margin_of_error = t_value * (standard_deviation / (sample_size ** 0.5))
        elif calculation_type == "Proportion":
            z_value = norm.ppf(1 - significance_level / 2)
            margin_of_error = z_value * ((sample_mean_or_proportion * (1 - sample_mean_or_proportion)) / sample_size) ** 0.5

        # Results
        lower_bound = sample_mean_or_proportion - margin_of_error
        upper_bound = sample_mean_or_proportion + margin_of_error

        st.success(f"The confidence interval is: [{lower_bound:.4f}, {upper_bound:.4f}]")