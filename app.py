import streamlit as st
from scipy.stats import norm, t

# Valores por defecto
DEFAULTS = {
    "sample_mean_or_proportion": 0.0,
    "significance_level": "",
    "standard_deviation": 0.0,
    "sample_size": 1,
    "calculation_type": ""
}

# Función para resetear variables
def reset_fields():
    for key, value in DEFAULTS.items():
        if key in st.session_state:
            del st.session_state[key]

# Título
st.title("Confidence Interval (CI) Calculator")

# Controles principales
with st.sidebar:
    calculation_type = st.selectbox(
        "What would you like to calculate?",
        ["", "Mean", "Proportion"],
        key="calculation_type"
    )

# Inputs
if calculation_type == "Proportion":
    sample_mean_or_proportion = st.number_input(
        "Enter the sample proportion (0 to 1):",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get("sample_mean_or_proportion", 0.0),
        key="sample_mean_or_proportion"
    )
elif calculation_type == "Mean":
    sample_mean_or_proportion = st.number_input(
        "Enter the sample mean:",
        value=st.session_state.get("sample_mean_or_proportion", 0.0),
        key="sample_mean_or_proportion"
    )

significance_level = st.selectbox(
    "Select the significance level (α):",
    ["", 0.10, 0.05, 0.01],
    index=0 if "significance_level" not in st.session_state else [0.10, 0.05, 0.01].index(st.session_state["significance_level"]) + 1 if st.session_state["significance_level"] in [0.10, 0.05, 0.01] else 0,
    key="significance_level"
)

if calculation_type == "Mean":
    standard_deviation = st.number_input(
        "Enter the standard deviation:",
        min_value=0.0,
        value=st.session_state.get("standard_deviation", 0.0),
        key="standard_deviation"
    )

sample_size_label = "Enter the sample size"
if calculation_type == "Proportion":
    sample_size_label += " (recommended: ≥ 30 for better approximation)"

sample_size = st.number_input(
    sample_size_label,
    min_value=1,
    value=st.session_state.get("sample_size", 1),
    key="sample_size"
)

# Botones en una fila
col1, col2 = st.columns(2)

with col1:
    if st.button("Calculate"):
        # Validar
        if not calculation_type or significance_level == "" or sample_mean_or_proportion is None or \
           (calculation_type == "Mean" and st.session_state.get("standard_deviation", 0.0) == 0.0) or \
           not sample_size:
            st.error("Please complete all required information.")
        else:
            st.subheader("Input Summary:")
            st.write(f"- **Statistic Type:** {calculation_type}")
            st.write(f"- **Significance Level (α):** {significance_level}")
            st.write(f"- **Sample Mean/Proportion:** {sample_mean_or_proportion}")
            if calculation_type == "Mean":
                st.write(f"- **Standard Deviation:** {st.session_state.standard_deviation}")
            st.write(f"- **Sample Size:** {sample_size}")

            # Calcular IC
            if calculation_type == "Mean":
                if sample_size >= 30:
                    z = norm.ppf(1 - significance_level / 2)
                    moe = z * (st.session_state.standard_deviation / (sample_size ** 0.5))
                else:
                    t_val = t.ppf(1 - significance_level / 2, df=sample_size - 1)
                    moe = t_val * (st.session_state.standard_deviation / (sample_size ** 0.5))
            else:
                z = norm.ppf(1 - significance_level / 2)
                moe = z * ((sample_mean_or_proportion * (1 - sample_mean_or_proportion)) / sample_size) ** 0.5
                if sample_size < 30:
                    st.warning("Recommended sample size ≥ 30 for better approximation.")

            lower = sample_mean_or_proportion - moe
            upper = sample_mean_or_proportion + moe
            st.success(f"The confidence interval is: [{lower:.4f}, {upper:.4f}]")

with col2:
    if st.button("Reset"):
        reset_fields()
        st.info("Fields reset! You can now enter new values.")
        st.rerun()  # <-- esta línea fuerza la actualización complet