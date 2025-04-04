import streamlit as st
from scipy.stats import norm, t

# Inicializar una bandera para reset si no existe
if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = False

# Función para simular reset (borrar claves específicas)
def soft_reset():
    keys_to_reset = [
        "sample_mean_or_proportion",
        "significance_level",
        "standard_deviation",
        "sample_size",
        "calculation_type"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.reset_flag = True

# Botón para resetear
if st.button("Reset"):
    soft_reset()

# Evitar mostrar widgets cuando se ha hecho reset en este ciclo
if not st.session_state.reset_flag:

    # Sidebar para seleccionar el tipo de cálculo
    with st.sidebar:
        calculation_type = st.selectbox(
            "What would you like to calculate?",
            ["", "Mean", "Proportion"],
            key="calculation_type"
        )

    st.title("Confidence Interval (CI) Calculator")

    # Inputs
    if st.session_state.get("calculation_type") == "Proportion":
        st.number_input(
            "Enter the sample proportion (values must be between 0 and 1):",
            min_value=0.0,
            max_value=1.0,
            key="sample_mean_or_proportion"
        )
    elif st.session_state.get("calculation_type") == "Mean":
        st.number_input(
            "Enter the sample mean:",
            key="sample_mean_or_proportion"
        )

    st.selectbox(
        "Select the significance level (α):",
        ["", 0.10, 0.05, 0.01],
        key="significance_level"
    )

    if st.session_state.get("calculation_type") == "Mean":
        st.number_input(
            "Enter the standard deviation:",
            min_value=0.0,
            key="standard_deviation"
        )

    sample_size_label = "Enter the sample size"
    if st.session_state.get("calculation_type") == "Proportion":
        sample_size_label += " (recommended: ≥ 30 for better approximation)"

    st.number_input(
        sample_size_label,
        min_value=1,
        key="sample_size"
    )

    # Botón para calcular
    if st.button("Calculate"):
        tipo = st.session_state.get("calculation_type")
        prop = st.session_state.get("sample_mean_or_proportion")
        alpha = st.session_state.get("significance_level")
        std_dev = st.session_state.get("standard_deviation")
        n = st.session_state.get("sample_size")

        if not tipo or alpha == "" or n is None or \
           (tipo == "Mean" and std_dev is None) or \
           (tipo == "Proportion" and (prop < 0 or prop > 1)):
            st.error("Please complete all required information.")
        else:
            st.subheader("Input Summary:")
            st.write(f"- **Statistic Type:** {tipo}")
            st.write(f"- **Significance Level (α):** {alpha}")
            st.write(f"- **Sample Mean/Proportion:** {prop}")
            if tipo == "Mean":
                st.write(f"- **Standard Deviation:** {std_dev}")
            st.write(f"- **Sample Size:** {n}")

            # Cálculo del intervalo de confianza
            if tipo == "Mean":
                if n >= 30:
                    z_value = norm.ppf(1 - alpha / 2)
                    margin_of_error = z_value * (std_dev / (n ** 0.5))
                else:
                    t_value = t.ppf(1 - alpha / 2, df=n - 1)
                    margin_of_error = t_value * (std_dev / (n ** 0.5))
            else:  # Proportion
                z_value = norm.ppf(1 - alpha / 2)
                margin_of_error = z_value * ((prop * (1 - prop)) / n) ** 0.5
                if n < 30:
                    st.warning("For proportions, it is recommended to have a sample size of at least 30.")

            lower = prop - margin_of_error
            upper = prop + margin_of_error
            st.success(f"The confidence interval is: [{lower:.4f}, {upper:.4f}]")

else:
    st.info("Inputs reset. Please re-enter your values.")