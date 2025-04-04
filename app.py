import streamlit as st
from scipy.stats import norm, t

# Inicializar session_state solo si no existe
defaults = {
    "calculation_type": "",
    "sample_mean_or_proportion": 0.0,
    "significance_level": "",
    "standard_deviation": 0.0,
    "sample_size": 1,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Función para resetear sin usar experimental_rerun
def reset_fields():
    for key, value in defaults.items():
        st.session_state[key] = value

# Título de la app
st.title("Confidence Interval (CI) Calculator")

# Sidebar para seleccionar el tipo de cálculo
st.session_state.calculation_type = st.sidebar.selectbox(
    "What would you like to calculate?",
    ["", "Mean", "Proportion"],
    key="calculation_type"
)

# Entradas según el tipo
if st.session_state.calculation_type == "Proportion":
    st.number_input(
        "Enter the sample proportion (0 to 1):",
        min_value=0.0,
        max_value=1.0,
        key="sample_mean_or_proportion"
    )
elif st.session_state.calculation_type == "Mean":
    st.number_input(
        "Enter the sample mean:",
        key="sample_mean_or_proportion"
    )

st.selectbox(
    "Select the significance level (α):",
    ["", 0.10, 0.05, 0.01],
    key="significance_level"
)

if st.session_state.calculation_type == "Mean":
    st.number_input(
        "Enter the standard deviation:",
        min_value=0.0,
        key="standard_deviation"
    )

sample_size_label = "Enter the sample size"
if st.session_state.calculation_type == "Proportion":
    sample_size_label += " (recommended: ≥ 30)"

st.number_input(
    sample_size_label,
    min_value=1,
    key="sample_size"
)

# Botones en una misma fila
col1, col2 = st.columns(2)
with col1:
    if st.button("Calculate"):
        calc = st.session_state.calculation_type
        mean_or_prop = st.session_state.sample_mean_or_proportion
        alpha = st.session_state.significance_level
        std_dev = st.session_state.standard_deviation
        n = st.session_state.sample_size

        if not calc or alpha == "" or mean_or_prop is None or (calc == "Mean" and std_dev == 0.0):
            st.error("Please complete all required information.")
        else:
            st.subheader("Input Summary:")
            st.write(f"- **Statistic Type:** {calc}")
            st.write(f"- **Significance Level (α):** {alpha}")
            st.write(f"- **Sample Mean/Proportion:** {mean_or_prop}")
            if calc == "Mean":
                st.write(f"- **Standard Deviation:** {std_dev}")
            st.write(f"- **Sample Size:** {n}")

            if calc == "Mean":
                if n >= 30:
                    z = norm.ppf(1 - alpha / 2)
                    moe = z * (std_dev / (n ** 0.5))
                else:
                    t_val = t.ppf(1 - alpha / 2, df=n - 1)
                    moe = t_val * (std_dev / (n ** 0.5))
            else:
                z = norm.ppf(1 - alpha / 2)
                moe = z * ((mean_or_prop * (1 - mean_or_prop)) / n) ** 0.5
                if n < 30:
                    st.warning("Recommended sample size ≥ 30 for better approximation.")

            lower = mean_or_prop - moe
            upper = mean_or_prop + moe

            st.success(f"The confidence interval is: [{lower:.4f}, {upper:.4f}]")

with col2:
    if st.button("Reset"):
        reset_fields()
        st.experimental_set_query_params()  # Forzar UI a recargar con estado limpio