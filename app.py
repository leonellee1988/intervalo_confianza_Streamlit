import streamlit as st
from scipy.stats import norm, t

# Función para inicializar los valores predeterminados en session_state
def initialize_session_state():
    if "calculation_type" not in st.session_state:
        st.session_state["calculation_type"] = ""
    if "sample_mean_or_proportion" not in st.session_state:
        st.session_state["sample_mean_or_proportion"] = 0.0
    if "significance_level" not in st.session_state:
        st.session_state["significance_level"] = ""
    if "standard_deviation" not in st.session_state:
        st.session_state["standard_deviation"] = 0.0
    if "sample_size" not in st.session_state:
        st.session_state["sample_size"] = 1

# Llamar la función para inicializar los valores en session_state
initialize_session_state()

# Función para limpiar los inputs
def clear_inputs():
    st.session_state["calculation_type"] = ""
    st.session_state["sample_mean_or_proportion"] = 0.0
    st.session_state["significance_level"] = ""
    st.session_state["standard_deviation"] = 0.0
    st.session_state["sample_size"] = 1

# Título de la aplicación
st.title("Confidence Interval (CI) Calculator")

# Sidebar para seleccionar el tipo de cálculo
with st.sidebar:
    calculation_type = st.selectbox(
        "What would you like to calculate?",
        ["", "Mean", "Proportion"],  # Default blank value
        key="calculation_type"
    )

# Inputs principales:
sample_mean_or_proportion = st.number_input(
    "Enter the sample mean or proportion:",
    format="%.4f",
    value=st.session_state["sample_mean_or_proportion"],
    key="sample_mean_or_proportion"
)

significance_level = st.selectbox(
    "Select the significance level (α):",
    ["", 0.10, 0.05, 0.01],  # Default blank value
    key="significance_level"
)

standard_deviation = None
if st.session_state["calculation_type"] == "Mean":
    standard_deviation = st.number_input(
        "Enter the standard deviation:",
        format="%.4f",
        value=st.session_state["standard_deviation"],
        key="standard_deviation"
    )

# Validación dinámica del tamaño mínimo de la muestra
min_sample_size = 30 if st.session_state["calculation_type"] == "Proportion" else 1
sample_size = st.number_input(
    "Enter the sample size (must be ≥ 30 for proportions):",
    format="%d",
    min_value=min_sample_size,  # Restricción basada en el tipo de cálculo
    value=st.session_state["sample_size"],
    key="sample_size"
)

# Botón para calcular
if st.button("Calculate"):
    if not st.session_state["calculation_type"] or not st.session_state["sample_mean_or_proportion"] or \
       not st.session_state["significance_level"] or \
       (st.session_state["calculation_type"] == "Mean" and not st.session_state["standard_deviation"]) or \
       not st.session_state["sample_size"]:
        st.error("Please complete all required information.")
    else:
        # Cálculo del intervalo de confianza
        if st.session_state["calculation_type"] == "Mean":
            if sample_size >= 30:  # Uso de Z para muestras grandes
                z_value = norm.ppf(1 - st.session_state["significance_level"] / 2)
                margin_of_error = z_value * (st.session_state["standard_deviation"] / (sample_size ** 0.5))
            else:  # Uso de T para muestras pequeñas
                t_value = t.ppf(1 - st.session_state["significance_level"] / 2, df=sample_size - 1)
                margin_of_error = t_value * (st.session_state["standard_deviation"] / (sample_size ** 0.5))
        elif st.session_state["calculation_type"] == "Proportion":
            z_value = norm.ppf(1 - st.session_state["significance_level"] / 2)
            margin_of_error = z_value * ((st.session_state["sample_mean_or_proportion"] * (1 - st.session_state["sample_mean_or_proportion"])) / sample_size) ** 0.5

        # Resultados
        lower_bound = st.session_state["sample_mean_or_proportion"] - margin_of_error
        upper_bound = st.session_state["sample_mean_or_proportion"] + margin_of_error

        st.success(f"The confidence interval is: [{lower_bound:.4f}, {upper_bound:.4f}]")

# Botón para limpiar los inputs
if st.button("Clear"):
    clear_inputs()