import streamlit as st
import math

# Custom CSS for Google-inspired design with red theme
st.markdown("""
<style>
/* Base styles */
.stApp {
    font-family: 'Google Sans', sans-serif !important;
}
/* Title and header styling */
h1 {
    font-weight: 500 !important;
    font-size: 2.5rem !important;
    margin-bottom: 2rem !important;
    color: #2563eb !important;  /* Blue accent */
}
.subtitle {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    opacity: 0.8;
}
/* Button styling */
.stButton > button {
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    margin-top: 1rem !important;
    background-color: #2563eb !important;  
    color: white !important;
    border: none !important;
}
.stButton > button:hover {
    background-color: #1e4fd1 !important;  
    box-shadow: 0 2px 6px rgba(220, 38, 38, 0.3) !important;
}
/* Result box styling */
.result-box {
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
    text-align: center;
    font-size: 1.25rem;
    font-weight: 500;
    box-shadow: 0 4px 6px rgba(220, 38, 38, 0.1);
    border: 2px solid #2563eb;
}
/* Footer styling */
.footer {
    text-align: center;
    margin-top: 3rem;
    padding: 1rem;
    font-size: 0.9rem;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Conversion Type")
st.sidebar.markdown("Choose conversion type and units below")

conversion_type = st.sidebar.selectbox(
    "Select Conversion Type",
    ["Length", "Weight", "Temperature"],
    index=0,
    format_func=lambda x: f"📏 {x}" if x == "Length" else f"⚖️ {x}" if x == "Weight" else f"🌡️ {x}"
)

st.title("Unit Converter")
st.markdown('<p class="subtitle">Convert between different units with real-time updates</p>', unsafe_allow_html=True)

LENGTH_UNITS = {
    "Kilometer": 1000, "Meter": 1, "Centimeter": 0.01, "Millimeter": 0.001,
    "Micrometer": 0.000001, "Nanometer": 0.000000001, "Mile": 1609.344,
    "Yard": 0.9144, "Foot": 0.3048, "Inch": 0.0254, "Nautical Mile": 1852
}
WEIGHT_UNITS = {
    "Kilogram": 1000, "Gram": 1, "Milligram": 0.001,
    "Metric Ton": 1000000, "Pound": 453.592, "Ounce": 28.3495
}
TEMPERATURE_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]

def convert_length(value, from_unit, to_unit):
    meters = value * LENGTH_UNITS[from_unit]
    return meters / LENGTH_UNITS[to_unit]

def convert_weight(value, from_unit, to_unit):
    grams = value * WEIGHT_UNITS[from_unit]  # Sabse pehle grams me convert karo
    return grams / WEIGHT_UNITS[to_unit]  # Target unit me wapis convert karo

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value  # Agar same unit ho, kuch convert nahi karna

    # Celsius to other conversions
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9/5) + 32
    if from_unit == "Celsius" and to_unit == "Kelvin":
        return value + 273.15

    # Fahrenheit to other conversions
    if from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) * 5/9
    if from_unit == "Fahrenheit" and to_unit == "Kelvin":
        return (value - 32) * 5/9 + 273.15

    # Kelvin to other conversions
    if from_unit == "Kelvin" and to_unit == "Celsius":
        return value - 273.15
    if from_unit == "Kelvin" and to_unit == "Fahrenheit":
        return (value - 273.15) * 9/5 + 32

    return None  # Agar kuch na mile to return None

def format_number(number):
    if abs(number) < 0.000001:
        return f"{number:.8e}"
    elif abs(number) < 0.001:
        return f"{number:.6f}"
    elif abs(number) < 1:
        return f"{number:.4f}"
    elif abs(number) < 1000:
        return f"{number:.2f}"
    else:
        return f"{number:,.2f}"

# Session state default values for swap functionality
if "from_unit" not in st.session_state or conversion_type != st.session_state.get("last_conversion_type"):
    if conversion_type == "Length":
        st.session_state.from_unit = "Meter"
        st.session_state.to_unit = "Kilometer"
    elif conversion_type == "Weight":
        st.session_state.from_unit = "Gram"
        st.session_state.to_unit = "Kilogram"
    else:  # Temperature
        st.session_state.from_unit = "Celsius"
        st.session_state.to_unit = "Fahrenheit"
    st.session_state.last_conversion_type = conversion_type  # Store last selected type
if "to_unit" not in st.session_state:
    st.session_state.to_unit = "Kilometer"

# User input
input_value = st.number_input("Enter value", value=1.0, format="%f", key="input_value")

col1, col2 = st.columns(2)
with col1:
    units = {
        "Length": LENGTH_UNITS.keys(),
        "Weight": WEIGHT_UNITS.keys(),
        "Temperature": TEMPERATURE_UNITS
    }[conversion_type]
    from_unit = st.selectbox("From", options=list(units), key="from_unit_select", index=list(units).index(st.session_state.from_unit))

with col2:
    to_unit = st.selectbox("To", options=list(units), key="to_unit_select", index=list(units).index(st.session_state.to_unit))

# Conversion logic
if input_value is not None:
    result = None
    if conversion_type == "Length":
        result = convert_length(input_value, from_unit, to_unit)
    elif conversion_type == "Weight":
        result = convert_weight(input_value, from_unit, to_unit)
    else:  # Temperature
        result = convert_temperature(input_value, from_unit, to_unit)

    if result is not None:
        formatted_result = format_number(result)

# Swap button
if st.button("🔄 Swap Units"):
    st.session_state.from_unit, st.session_state.to_unit = st.session_state.to_unit, st.session_state.from_unit
    st.rerun()

# Display the result BELOW the swap button
if input_value is not None and result is not None:
    st.markdown(
        f"""
        <div class="result-box">
            {format_number(input_value)} {from_unit} = {formatted_result} {to_unit}
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("""<div class="footer">Built with Streamlit • Inspired by Google's Unit Converter</div>""", unsafe_allow_html=True)
