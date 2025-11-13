import streamlit as st
import pandas as pd
import plotly.express as px

# Create the BMI table as a dictionary
data = {
    "Classification": [
        "Underweight",
        "Normal",
        "Overweight",
        "Obese",
    ],
    "BMI range (kg/m²)": [
        "< 18.5",
        "18.5 – 24.9",
        "25 – 29.9",
        "30 >",
    ]
}

# Create a DataFrame
bmi_table = pd.DataFrame(data)


with open("style.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# --- App Configuration ---
st.set_page_config(page_title="Are You Fit?", page_icon="💪", layout="centered")

# --- App Title ---
st.title("💪 Are You Fit?")
st.write("Easily Calculate your BMI and see which category you fall into!!!")

# --- Input Section ---
st.header("Enter your details:")
col1, col2 = st.columns(2)

with col1:
    weight = st.number_input("Weight (kg):", min_value=0.0, format="%.2f")
with col2:
    height = st.number_input("Height (m):", min_value=0.0, format="%.2f")

# --- BMI Calculation ---
if st.button("🔍 Calculate BMI"):
    if height > 0:
        bmi = weight / (height ** 2)
        st.subheader(f"📊 Your BMI is: *{bmi:.2f}*")

        # Interpretation
        if bmi < 18.5:
            category = "Underweight"
            color = "blue"
            msg = "You are underweight 😕. Consider eating more nutritious food."
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
            color = "green"
            msg = "Great! You are in a healthy weight range 😊"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
            color = "orange"
            msg = "You are overweight 😬. Some exercise could help!"
        else:
            category = "Obese"
            color = "red"
            msg = "You are obese 😔. It may be good to consult a doctor."

        st.markdown(f"### 🧠 BMI Category: <span style='color:{color}'>{category}</span>", unsafe_allow_html=True)
        st.info(msg)

        # --- Chart ---
        st.header("📈 BMI Categories Chart")

        bmi_data = pd.DataFrame({
            "Category": ["Underweight", "Normal", "Overweight", "Obese"],
            "BMI Range": [18.5, 24.9, 29.9, 35]
        })

        fig = px.bar(
            bmi_data,
            x="Category",
            y="BMI Range",
            color="Category",
            text="BMI Range",
            color_discrete_map={
                "Underweight": "blue",
                "Normal": "green",
                "Overweight": "orange",
                "Obese": "red"
            },
            title="BMI Category Ranges"
        )

        fig.add_vline(x=list(bmi_data["Category"]).index(category),
                      line_color=color, line_dash="dash",
                      annotation_text=f"Your BMI ({bmi:.2f})",
                      annotation_position="top")

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Please enter a valid height greater than 0.")

st.table(bmi_table)