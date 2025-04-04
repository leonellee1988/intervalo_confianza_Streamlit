import streamlit as st
from scipy.stats import norm, t

# Inicializar valores predeterminados en session_state
def initialize_session_state():
    if "sample_mean_or_proportion_reset" not in st.session_state:
        st.session_state["sample_mean_or_proportion_reset"] = None
    if "significance_level_reset" not in st.session_state:
        st.session_state["significance_level_reset"] = ""
    if "standard_deviation_reset" not in st.session_state:
        st.session_state["standard_deviation_reset"] = None
    if "sample_size_reset" not in st.session_state:
        st.session_state["sample_size_reset"] = 1

initialize_session_state()

# Función para resetear valores sin modificar claves vinculadas a widgets
def reset_inputs():
    st.session_state["sample_mean_or_proportion_reset"] = None
    st.session_state["significance_level_reset"] = ""
    st.session_state["standard_deviation_reset"] = None
    st.session_state["sample_size_reset"] = 1

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
    sample_mean_or_proportion = st.number_input(
        "Enter the sample proportion (values must be between 0 and 1):",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state["sample_mean_or_proportion_reset"],  # Usando la clave dinámica
        key="sample_mean_or_proportion_reset"
    )
elif calculation_type == "Mean":
    sample_mean_or_proportion = st.number_input(
        "Enter the sample mean:",
        value=st.session_state["sample_mean_or_proportion_reset"],  # Usando la clave dinámica
        key="sample_mean_or_proportion_reset"
    )

significance_level = st.selectbox(
    "Select the significance level (α):",
    ["", 0.10, 0.05, 0.01],
    key="significance_level_reset"  # Usando la clave dinámica
)

standard_deviation = None
if calculation_type == "Mean":
    standard_deviation = st.number_input(
        "Enter the standard deviation:",
        min_value=0.0,
        value=st.session_state["standard_deviation_reset"],  # Usando la clave dinámica
        key="standard_deviation_reset"
    )

sample_size_label = "Enter the sample size"
if calculation_type == "Proportion":
    sample_size_label += " (recommended: ≥ 30 for better approximation)"

sample_size = st.number_input(
    sample_size_label,
    min_value=1,
    value=st.session_state["sample_size_reset"],  # Usando la clave dinámica
    key="sample_size_reset"
)

# Botón para calcular
if st.button("Calculate"):
    if not calculation_type or sample_mean_or_proportion is None or not significance_level or \
       (calculation_type == "Mean" and standard_deviation is None) or not sample_size:
        st.error("Please complete all required information.")
    else:
        # Mostrar resumen de los datos ingresados
        st.subheader("Input Summary:")
        st.write(f"- **Statistic Type:** {calculation_type}")
        st.write(f"- **Significance Level (α):** {significance_level}")
        st.write(f"- **Sample Mean/Proportion:** {sample_mean_or_proportion}")
        if calculation_type == "Mean":
            st.write(f"- **Standard Deviation:** {standard_deviation}")
        st.write(f"- **Sample Size:** {sample_size}")

        # Cálculo del intervalo de confianza
        if calculation_type == "Mean":
            if sample_size >= 30:
                z_value = norm.ppf(1 - significance_level / 2)
                margin_of_error = z_value * (standard_deviation / (sample_size ** 0.5))
            else:
                t_value = t.ppf(1 - significance_level / 2, df=sample_size - 1)
                margin_of_error = t_value * (standard_deviation / (sample_size ** 0.5))
        elif calculation_type == "Proportion":
            z_value = norm.ppf(1 - significance_level / 2)
            margin_of_error = z_value * ((sample_mean_or_proportion * (1 - sample_mean_or_proportion)) / sample_size) ** 0.5

            # Advertencia para muestras pequeñas
            if sample_size < 30:
                st.warning("For proportions, it is recommended to have a sample size of at least 30 for better approximation.")

        # Resultados del intervalo de confianza
        lower_bound = sample_mean_or_proportion - margin_of_error
        upper_bound = sample_mean_or_proportion + margin_of_error

        st.success(f"The confidence interval is: [{lower_bound:.4f}, {upper_bound:.4f}]")

        # Resetear valores después del cálculo
        reset_inputs()