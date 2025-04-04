import streamlit as st
from scipy.stats import norm, t

# Bandeja para controlar el reset
if "do_reset" not in st.session_state:
    st.session_state["do_reset"] = False

# Botón RESET: activa la bandera de reinicio y detiene la ejecución
if st.button("Reset"):
    st.session_state["do_reset"] = True
    st.stop()

# Si el reset fue solicitado, limpiamos todo y salimos
if st.session_state["do_reset"]:
    st.session_state.clear()  # limpia todas las claves
    st.experimental_rerun()  # <-- si tienes versión compatible, si no omite esta línea

# Título principal
st.title("Confidence Interval (CI) Calculator")

# Sidebar para seleccionar el tipo de cálculo
calculation_type = st.sidebar.selectbox(
    "What would you like to calculate?",
    ["", "Mean", "Proportion"],
    key="calculation_type"
)

# Inputs principales según el tipo de estadístico
if calculation_type == "Proportion":
    sample_mean_or_proportion = st.number_input(
        "Enter the sample proportion (0 to 1):",
        min_value=0.0,
        max_value=1.0,
        key="sample_mean_or_proportion"
    )
elif calculation_type == "Mean":
    sample_mean_or_proportion = st.number_input(
        "Enter the sample mean:",
        key="sample_mean_or_proportion"
    )

significance_level = st.selectbox(
    "Select the significance level (α):",
    ["", 0.10, 0.05, 0.01],
    key="significance_level"
)

standard_deviation = None
if calculation_type == "Mean":
    standard_deviation = st.number_input(
        "Enter the standard deviation:",
        min_value=0.0,
        key="standard_deviation"
    )

sample_size_label = "Enter the sample size"
if calculation_type == "Proportion":
    sample_size_label += " (recommended: ≥ 30)"

sample_size = st.number_input(
    sample_size_label,
    min_value=1,
    key="sample_size"
)

# Botón para calcular
if st.button("Calculate"):
    # Validación
    if not calculation_type or significance_level == "" or sample_size is None or \
       (calculation_type == "Mean" and standard_deviation is None) or \
       sample_mean_or_proportion is None:
        st.error("Please complete all required information.")
    else:
        st.subheader("Input Summary:")
        st.write(f"- **Statistic Type:** {calculation_type}")
        st.write(f"- **Significance Level (α):** {significance_level}")
        st.write(f"- **Sample Mean/Proportion:** {sample_mean_or_proportion}")
        if calculation_type == "Mean":
            st.write(f"- **Standard Deviation:** {standard_deviation}")
        st.write(f"- **Sample Size:** {sample_size}")

        # Cálculo del intervalo
        if calculation_type == "Mean":
            if sample_size >= 30:
                z = norm.ppf(1 - significance_level / 2)
                moe = z * (standard_deviation / (sample_size ** 0.5))
            else:
                t_val = t.ppf(1 - significance_level / 2, df=sample_size - 1)
                moe = t_val * (standard_deviation / (sample_size ** 0.5))
        else:
            z = norm.ppf(1 - significance_level / 2)
            moe = z * ((sample_mean_or_proportion * (1 - sample_mean_or_proportion)) / sample_size) ** 0.5
            if sample_size < 30:
                st.warning("Recommended sample size ≥ 30 for better approximation.")

        lower = sample_mean_or_proportion - moe
        upper = sample_mean_or_proportion + moe

        st.success(f"The confidence interval is: [{lower:.4f}, {upper:.4f}]")