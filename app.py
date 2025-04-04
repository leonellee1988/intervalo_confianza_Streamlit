import streamlit as st
from scipy.stats import norm, t

# Inicializar valores predeterminados en session_state
def initialize_session_state():
    if "calculation_type_reset" not in st.session_state:
        st.session_state["calculation_type_reset"] = ""
    if "sample_mean_or_proportion_reset" not in st.session_state:
        st.session_state["sample_mean_or_proportion_reset"] = ""
    if "significance_level_reset" not in st.session_state:
        st.session_state["significance_level_reset"] = ""
    if "standard_deviation_reset" not in st.session_state:
        st.session_state["standard_deviation_reset"] = ""
    if "sample_size_reset" not in st.session_state:
        st.session_state["sample_size_reset"] = ""

# Llamar la función para inicializar los valores
initialize_session_state()

# Título de la aplicación
st.title("Confidence Interval (CI) Calculator")

# Sidebar para seleccionar el tipo de cálculo
calculation_type = st.selectbox(
    "What would you like to calculate?",
    ["", "Mean", "Proportion"],  # Default blank value
    key="calculation_type_reset"  # Usamos una clave única para la limpieza
)

# Inputs principales
sample_mean_or_proportion = st.number_input(
    "Enter the sample mean or proportion:",
    format="%.4f",
    value=st.session_state["sample_mean_or_proportion_reset"],
    key="sample_mean_or_proportion_reset"
)

significance_level = st.selectbox(
    "Select the significance level (α):",
    ["", 0.10, 0.05, 0.01],  # Default blank value
    key="significance_level_reset"
)

standard_deviation = None
if calculation_type == "Mean":
    standard_deviation = st.number_input(
        "Enter the standard deviation:",
        format="%.4f",
        value=st.session_state["standard_deviation_reset"],
        key="standard_deviation_reset"
    )

# Etiqueta condicional para el tamaño de muestra
sample_size_label = "Enter the sample size"
if calculation_type == "Proportion":
    sample_size_label += " (must be ≥ 30 for proportions)"

min_sample_size = 30 if calculation_type == "Proportion" else 1
sample_size = st.number_input(
    sample_size_label,
    format="%d",
    min_value=min_sample_size,  # Restricción basada en el tipo de cálculo
    value=st.session_state["sample_size_reset"],
    key="sample_size_reset"
)

# Botón para calcular
if st.button("Calculate"):
    if not calculation_type or not sample_mean_or_proportion or not significance_level or \
       (calculation_type == "Mean" and not standard_deviation) or not sample_size:
        st.error("Please complete all required information.")
    else:
        # Cálculo del intervalo de confianza
        if calculation_type == "Mean":
            if sample_size >= 30:  # Uso de Z para muestras grandes
                z_value = norm.ppf(1 - significance_level / 2)
                margin_of_error = z_value * (standard_deviation / (sample_size ** 0.5))
            else:  # Uso de T para muestras pequeñas
                t_value = t.ppf(1 - significance_level / 2, df=sample_size - 1)
                margin_of_error = t_value * (standard_deviation / (sample_size ** 0.5))
        elif calculation_type == "Proportion":
            z_value = norm.ppf(1 - significance_level / 2)
            margin_of_error = z_value * ((sample_mean_or_proportion * (1 - sample_mean_or_proportion)) / sample_size) ** 0.5

        # Resultados
        lower_bound = sample_mean_or_proportion - margin_of_error
        upper_bound = sample_mean_or_proportion + margin_of_error

        st.success(f"The confidence interval is: [{lower_bound:.4f}, {upper_bound:.4f}]")

# Botón para limpiar los inputs
if st.button("Clear"):
    # Resetear los valores sin modificar widgets ya instanciados
    st.session_state["calculation_type_reset"] = ""
    st.session_state["sample_mean_or_proportion_reset"] = ""
    st.session_state["significance_level_reset"] = ""
    st.session_state["standard_deviation_reset"] = ""
    st.session_state["sample_size_reset"] = ""