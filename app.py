import streamlit as st
from scipy.stats import norm, t

# Función para resetear session_state de forma segura
def reset_session_state():
    st.session_state.clear()
    st.experimental_rerun()

# Título de la aplicación
st.title("Confidence Interval (CI) Calculator")

# Sidebar para seleccionar el tipo de cálculo
with st.sidebar:
    calculation_type = st.selectbox(
        "What would you like to calculate?",
        ["", "Mean", "Proportion"]
    )

# Inputs principales
if calculation_type == "Proportion":
    st.number_input(
        "Enter the sample proportion (values must be between 0 and 1):",
        min_value=0.0,
        max_value=1.0,
        key="sample_mean_or_proportion"
    )
elif calculation_type == "Mean":
    st.number_input(
        "Enter the sample mean:",
        key="sample_mean_or_proportion"
    )

st.selectbox(
    "Select the significance level (α):",
    ["", 0.10, 0.05, 0.01],
    key="significance_level"
)

if calculation_type == "Mean":
    st.number_input(
        "Enter the standard deviation:",
        min_value=0.0,
        key="standard_deviation"
    )

sample_size_label = "Enter the sample size"
if calculation_type == "Proportion":
    sample_size_label += " (recommended: ≥ 30 for better approximation)"

st.number_input(
    sample_size_label,
    min_value=1,
    key="sample_size"
)

# Botones de acción
col1, col2 = st.columns(2)

with col1:
    if st.button("Calculate"):
        # Extraer valores desde session_state
        p_or_mean = st.session_state.get("sample_mean_or_proportion", None)
        alpha = st.session_state.get("significance_level", "")
        std_dev = st.session_state.get("standard_deviation", None)
        n = st.session_state.get("sample_size", None)

        if not calculation_type or alpha == "" or n is None or \
           (calculation_type == "Mean" and std_dev is None) or \
           (calculation_type == "Proportion" and (p_or_mean < 0 or p_or_mean > 1)):
            st.error("Please complete all required information.")
        else:
            st.subheader("Input Summary:")
            st.write(f"- **Statistic Type:** {calculation_type}")
            st.write(f"- **Significance Level (α):** {alpha}")
            st.write(f"- **Sample Mean/Proportion:** {p_or_mean}")
            if calculation_type == "Mean":
                st.write(f"- **Standard Deviation:** {std_dev}")
            st.write(f"- **Sample Size:** {n}")

            # Cálculo del intervalo de confianza
            if calculation_type == "Mean":
                if n >= 30:
                    z_value = norm.ppf(1 - alpha / 2)
                    margin_of_error = z_value * (std_dev / (n ** 0.5))
                else:
                    t_value = t.ppf(1 - alpha / 2, df=n - 1)
                    margin_of_error = t_value * (std_dev / (n ** 0.5))
            elif calculation_type == "Proportion":
                z_value = norm.ppf(1 - alpha / 2)
                margin_of_error = z_value * ((p_or_mean * (1 - p_or_mean)) / n) ** 0.5
                if n < 30:
                    st.warning("For proportions, it is recommended to have a sample size of at least 30 for better approximation.")

            lower_bound = p_or_mean - margin_of_error
            upper_bound = p_or_mean + margin_of_error

            st.success(f"The confidence interval is: [{lower_bound:.4f}, {upper_bound:.4f}]")

with col2:
    if st.button("Reset"):
        reset_session_state()