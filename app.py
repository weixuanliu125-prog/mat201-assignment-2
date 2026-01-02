import streamlit as st
import numpy as np

st.set_page_config(page_title="MAT201 Differential Calculator", layout="wide")

st.title("📐 MAT201 Differential Visualization")
st.markdown("### Assignment 2 - Topic: Differentials")

# Simple interface
col1, col2 = st.columns(2)

with col1:
    x = st.number_input("x₀", value=1.0, step=0.1)
    y = st.number_input("y₀", value=1.0, step=0.1)

with col2:
    dx = st.number_input("dx", value=0.1, step=0.01)
    dy = st.number_input("dy", value=0.1, step=0.01)

# Simple differential calculation (no sympy for now)
st.markdown("### Differential Calculation")
st.latex(r"f(x,y) = x^2 + y^2")
st.latex(r"f_x = 2x, \quad f_y = 2y")
st.latex(r"df = f_x dx + f_y dy = 2x\,dx + 2y\,dy")

# Calculate
f = x**2 + y**2
f_x = 2*x
f_y = 2*y
df = f_x*dx + f_y*dy
f_new = (x+dx)**2 + (y+dy)**2
delta_f = f_new - f

# Display results
st.metric("f(x₀,y₀)", f"{f:.4f}")
st.metric("∂f/∂x", f"{f_x:.4f}")
st.metric("∂f/∂y", f"{f_y:.4f}")
st.metric("Differential df", f"{df:.4f}")
st.metric("Actual Δf", f"{delta_f:.4f}")
st.metric("Error", f"{abs(delta_f - df):.6f}")

st.success("✅ Application deployed successfully!")
st.info("This is a simplified version for deployment testing.")

