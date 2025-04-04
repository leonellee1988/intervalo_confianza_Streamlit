# Cargar librerias (considerar en el archivo requirements.txt):
import streamlit as st
from scipy.stats import norm, t

# Titulo de la aplicación:
st.title("Confidence Interval (CI) Calculator")

# Segmentadores (barra lateral)
with st.sidebar:
    # Segmentador 1: tipo de calculo (media o proporción):
    calculation_type = st.selectbox(
        "What would you like to calculate?",
        ["", "Mean", "Proportion"]
    )

    # Segmentador 2: tamaño de la muestra:
    sample_size_type = None
    if calculation_type == "Mean":
        sample_size_type = st.selectbox(
            "What is your sample size?",
            ["", "Large (≥ 30)", "Small (< 30)"]
        )

# Sección principal de la App:

# Input: ingreso de la media o proporción:
sample_mean_or_proportion = st.number_input(
    "Enter the sample mean or proportion:",
    format="%.4f",
    value=0.0
)

# Input: ingreso del nivel de significancia:
significance_level = st.selectbox(
    "Select the significance level (α):",
    ["", 0.10, 0.05, 0.01]
)

# Input: ingreso de la desviación estándar (aplica para medias):
standard_deviation = None
if calculation_type == "Mean":
    standard_deviation = st.number_input(
        "Enter the standard deviation:",
        format="%.4f",
        value=0.0  # Initial value set to 0.0
    )

# Input: ingreso tamaño de la muestra:
sample_size = st.number_input(
    "Enter the sample size:",
    format="%d",
    min_value=1
)

# Validación del tamaño de la muestra:
if sample_size_type == "Large (≥ 30)" and sample_size < 30:
    st.error("Sample size must be at least 30 for large samples.")

# Botón de calculo:
if st.button("Calculate"):
    if not calculation_type or not sample_mean_or_proportion or not significance_level or \
       (calculation_type == "Mean" and not standard_deviation) or not sample_size or \
       (calculation_type == "Mean" and not sample_size_type):
        st.error("Please complete all required information.")
    else:
        # Calculo del intervalo de confianza:
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

        # Resultado
        lower_bound = sample_mean_or_proportion - margin_of_error
        upper_bound = sample_mean_or_proportion + margin_of_error

        st.success(f"The confidence interval is: [{lower_bound:.4f}, {upper_bound:.4f}]")