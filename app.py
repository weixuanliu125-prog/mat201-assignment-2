import streamlit as st
import numpy as np
import sympy as sp

st.title("MAT201 Differential Calculator")
st.write("Application deployed successfully!")

# Simple differential example
x, y = sp.symbols('x y')
f = x**2 + y**2

st.latex(f"f(x,y) = {sp.latex(f)}")
st.latex(r"df = \frac{\partial f}{\partial x}dx + \frac{\partial f}{\partial y}dy")
st.latex(f"df = 2x\,dx + 2y\,dy")

st.success("✅ Deployment successful! This proves the app works.")
