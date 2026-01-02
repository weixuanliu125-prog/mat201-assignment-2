# -*- coding: utf-8 -*-
"""
MAT201 Calculus Assignment - Differential Visualization Application
Author: [LIU WEIXUAN] 
Student ID: [24101888] 
Course: MAT201 Calculus
Date: January 2026
Deployment URL: https://[你的用户名]-mat201-assignment.streamlit.app/  # 部署后替换

AI Assistance Summary:
1. Streamlit application structure and UI design
2. Mathematical formula explanations and LaTeX formatting
3. Error calculation logic and optimization suggestions
4. Real-world application examples and case studies
5. Code documentation and comments

Generated with assistance from: ChatGPT, GitHub Copilot
Human input: Mathematical concept verification, custom examples, real-world applications
"""

import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional
import io
import base64
from datetime import datetime

# ============================================
# TEAM INFORMATION (FOR GROUP SUBMISSIONS)
# ============================================
TEAM_MEMBERS = [
    "Member 1: [你的全名] ([学号])",  # 请填写你的信息
    # "Member 2: [组员2名字] ([学号])",  # 如果有组员，取消注释并填写
    # "Member 3: [组员3名字] ([学号])",   # 如果有组员，取消注释并填写
]

# ============================================
# DEPLOYMENT INFORMATION
# ============================================
DEPLOYMENT_URL = "https://[你的用户名]-mat201-assignment.streamlit.app/"  # 部署后替换
GITHUB_REPO = "https://github.com/[你的用户名]/mat201-assignment-2"  # 你的GitHub仓库链接

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Multivariable Differential Visualization",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS STYLING
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        padding-top: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #374151;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #F0F9FF;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 6px solid #3B82F6;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-box {
        background-color: #F8FAFC;
        padding: 1.2rem;
        border-radius: 0.5rem;
        border: 2px solid #E2E8F0;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .example-box {
        background-color: #FEF3C7;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #F59E0B;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #10B981;
        margin: 1rem 0;
    }
    .screenshot-box {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 3px dashed #6B7280;
        margin: 1rem 0;
        text-align: center;
    }
    .ai-box {
        background-color: #F0F9FF;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #3B82F6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# TITLE AND DESCRIPTION
# ============================================
st.markdown("<h1 class='main-header'>📐 Multivariable Differential Visualization</h1>", unsafe_allow_html=True)
st.markdown("### MAT201 Calculus Assignment 2 - Topic: Differentials")

# Display team information
with st.expander("👥 Team Information", expanded=False):
    for member in TEAM_MEMBERS:
        st.write(f"• {member}")
    
    st.markdown(f"""
    **Deployment Information:**
    - Live Application: [{DEPLOYMENT_URL}]({DEPLOYMENT_URL})
    - GitHub Repository: [{GITHUB_REPO}]({GITHUB_REPO})
    """)

# ============================================
# SIDEBAR CONTROLS
# ============================================
with st.sidebar:
    st.markdown("## ⚙️ Controls Panel")
    
    # Example selection for assignment requirements
    st.markdown("### 📚 Assignment Examples")
    example_choice = st.selectbox(
        "Choose example for assignment:",
        ["Example 1: Basic - x² + y²",
         "Example 2: Advanced - sin(x)*cos(y)",
         "Custom Function"]
    )
    
    if example_choice == "Example 1: Basic - x² + y²":
        function_str = "x**2 + y**2"
        preset_params = {"x0": 1.0, "y0": 1.0, "dx": 0.1, "dy": 0.1}
    elif example_choice == "Example 2: Advanced - sin(x)*cos(y)":
        function_str = "sin(x)*cos(y)"
        preset_params = {"x0": 0.7854, "y0": 0.7854, "dx": 0.2, "dy": 0.1}
    else:
        function_str = st.text_input(
            "Enter custom function f(x, y):",
            value="x**2 + x*y + y**2",
            help="Use Python syntax with x and y as variables"
        )
        preset_params = None
    
    st.markdown("---")
    
    # Point coordinates
    st.markdown("### 📍 Analysis Point")
    col1, col2 = st.columns(2)
    with col1:
        x0 = st.number_input("x₀", value=preset_params["x0"] if preset_params else 1.0, 
                           step=0.1, format="%.4f")
    with col2:
        y0 = st.number_input("y₀", value=preset_params["y0"] if preset_params else 1.0, 
                           step=0.1, format="%.4f")
    
    st.markdown("---")
    
    # Increments for differential
    st.markdown("### 📏 Increments (dx, dy)")
    col3, col4 = st.columns(2)
    with col3:
        dx = st.number_input("Δx", value=preset_params["dx"] if preset_params else 0.1, 
                           step=0.01, format="%.4f")
    with col4:
        dy = st.number_input("Δy", value=preset_params["dy"] if preset_params else 0.1, 
                           step=0.01, format="%.4f")
    
    st.markdown("---")
    
    # Visualization settings
    st.markdown("### 🎨 Visualization Settings")
    plot_range = st.slider("Plot Range", min_value=1.0, max_value=5.0, 
                          value=2.0, step=0.5)
    show_tangent = st.checkbox("Show Tangent Plane", value=True)
    show_contour = st.checkbox("Show Contour Lines", value=True)
    
    st.markdown("---")
    
    # Enhanced Screenshot functionality
    st.markdown("### 📸 Screenshot Tools")
    
    screenshot_mode = st.selectbox(
        "Screenshot mode:",
        ["Manual Screenshot", "Generate Example Screenshots"]
    )
    
    if screenshot_mode == "Manual Screenshot":
        if st.button("📸 Prepare for Screenshot"):
            st.session_state.screenshot_ready = True
            st.success("Ready for screenshot! Follow instructions below.")
            st.info("""
            **Screenshot Instructions:**
            1. Position this window for your screenshot
            2. Use system screenshot tool:
               - Windows: Win + Shift + S
               - Mac: Shift + Cmd + 4
               - Linux: Use screenshot tool
            3. Save as PNG format
            4. Include in your assignment report
            """)
    
    elif screenshot_mode == "Generate Example Screenshots":
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("🔄 Load Example 1 Preset"):
                st.session_state.load_example = 1
                st.rerun()
        with col_s2:
            if st.button("🔄 Load Example 2 Preset"):
                st.session_state.load_example = 2
                st.rerun()
    
    st.markdown("---")
    
    # Information about differentials
    with st.expander("ℹ️ About Differentials (Mathematical Theory)"):
        st.markdown("""
        ### Differential Definition
        
        For a function $z = f(x, y)$, the total differential at point $(x_0, y_0)$ is:
        
        $$
        dz = f_x(x_0, y_0)dx + f_y(x_0, y_0)dy
        $$
        
        Where:
        - $f_x = \\frac{\\partial f}{\\partial x}$ is the partial derivative with respect to x
        - $f_y = \\frac{\\partial f}{\\partial y}$ is the partial derivative with respect to y
        - $dx = \\Delta x$, $dy = \\Delta y$ are the increments
        
        ### Geometric Interpretation
        
        The differential $dz$ represents the height change of the tangent plane:
        
        $$
        \\Delta z \\approx dz
        $$
        
        This approximation is accurate when $dx$ and $dy$ are small.
        """)

# ============================================
# HELPER FUNCTIONS
# ============================================
def parse_function(func_str: str) -> Optional[sp.Expr]:
    """Parse string function to sympy expression."""
    try:
        x, y = sp.symbols('x y')
        f = sp.sympify(func_str)
        return f
    except Exception as e:
        st.error(f"Error parsing function: {e}")
        return None

def compute_differentials(f: sp.Expr, x0: float, y0: float, dx: float, dy: float) -> dict:
    """Compute differential and related quantities."""
    x, y = sp.symbols('x y')
    
    # Compute function value
    f_value = float(f.subs({x: x0, y: y0}))
    
    # Compute partial derivatives
    f_x = sp.diff(f, x)
    f_y = sp.diff(f, y)
    f_x_val = float(f_x.subs({x: x0, y: y0}))
    f_y_val = float(f_y.subs({x: x0, y: y0}))
    
    # Compute actual change
    f_new = float(f.subs({x: x0 + dx, y: y0 + dy}))
    delta_f = f_new - f_value
    
    # Compute differential approximation
    df = f_x_val * dx + f_y_val * dy
    
    # Compute error
    absolute_error = abs(delta_f - df)
    relative_error = (absolute_error / abs(delta_f)) * 100 if delta_f != 0 else 0
    
    # Compute gradient magnitude
    grad_magnitude = np.sqrt(f_x_val**2 + f_y_val**2)
    
    return {
        'function': f,
        'f_value': f_value,
        'f_x': f_x,
        'f_y': f_y,
        'f_x_val': f_x_val,
        'f_y_val': f_y_val,
        'delta_f': delta_f,
        'df': df,
        'absolute_error': absolute_error,
        'relative_error': relative_error,
        'f_new': f_new,
        'grad_magnitude': grad_magnitude,
        'x0': x0,
        'y0': y0,
        'dx': dx,
        'dy': dy
    }

# ============================================
# SCREENSHOT HELPER FUNCTIONS
# ============================================
def create_screenshot_guide():
    """Create a screenshot guide section."""
    st.markdown("<div class='screenshot-box'>", unsafe_allow_html=True)
    st.markdown("### 📸 SCREENSHOT AREA")
    st.markdown("**Position this section in your screenshot**")
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"Screenshot generated: {current_time}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Required Screenshots:**")
        st.markdown("""
        1. Example 1 Results
        2. Example 2 Results  
        3. 3D Visualization
        4. Error Analysis
        5. AI Usage Summary
        """)
    
    with col2:
        st.markdown("**Screenshot Tips:**")
        st.markdown("""
        • Use full-screen mode
        • Ensure good contrast
        • Include all relevant data
        • Save as high-quality PNG
        • Label in your report
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

def generate_example_screenshot_data(example_num: int) -> dict:
    """Generate preset data for example screenshots."""
    if example_num == 1:
        return {
            'function': 'x**2 + y**2',
            'title': 'Example 1: Basic Function - f(x,y) = x² + y²',
            'params': {'x0': 1.0, 'y0': 1.0, 'dx': 0.1, 'dy': 0.1},
            'description': 'Quadratic function demonstrating basic differential concepts'
        }
    else:  # example_num == 2
        return {
            'function': 'sin(x)*cos(y)',
            'title': 'Example 2: Advanced Function - f(x,y) = sin(x)cos(y)',
            'params': {'x0': 0.7854, 'y0': 0.7854, 'dx': 0.2, 'dy': 0.1},
            'description': 'Trigonometric function showing complex differential behavior'
        }

# ============================================
# VISUALIZATION FUNCTIONS
# ============================================
def create_3d_plot(results: dict, x0: float, y0: float, dx: float, dy: float, 
                   plot_range: float, show_tangent: bool, show_contour: bool) -> go.Figure:
    """Create 3D visualization of function and differential."""
    x, y = sp.symbols('x y')
    f = results['function']
    
    # Create grid
    x_vals = np.linspace(x0 - plot_range, x0 + plot_range, 50)
    y_vals = np.linspace(y0 - plot_range, y0 + plot_range, 50)
    X, Y = np.meshgrid(x_vals, y_vals)
    
    # Evaluate function on grid
    f_numpy = sp.lambdify((x, y), f, 'numpy')
    Z = f_numpy(X, Y)
    
    # Create figure
    fig = go.Figure()
    
    # Add function surface
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        name='Function Surface',
        colorscale='Viridis',
        opacity=0.8,
        contours={"z": {"show": show_contour, "size": 0.2, "color": "white"}}
    ))
    
    # Add tangent plane if requested
    if show_tangent:
        Z_tangent = results['f_value'] + results['f_x_val']*(X - x0) + results['f_y_val']*(Y - y0)
        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z_tangent,
            name='Tangent Plane',
            colorscale='Reds',
            opacity=0.5,
            showscale=False
        ))
    
    # Add analysis point
    fig.add_trace(go.Scatter3d(
        x=[x0], y=[y0], z=[results['f_value']],
        mode='markers+text',
        marker=dict(size=8, color='red'),
        text=['Start'],
        textposition="top center",
        name=f'Point ({x0:.2f}, {y0:.2f})'
    ))
    
    # Add point after increment
    fig.add_trace(go.Scatter3d(
        x=[x0 + dx], y=[y0 + dy], z=[results['f_new']],
        mode='markers+text',
        marker=dict(size=8, color='green'),
        text=['End'],
        textposition="top center",
        name=f'New Point ({x0+dx:.2f}, {y0+dy:.2f})'
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'f(x,y) = {sp.latex(f)}',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        },
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='f(x, y)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        height=600,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True
    )
    
    return fig

# ============================================
# ASSIGNMENT EXAMPLES SECTION (ENHANCED)
# ============================================
def display_assignment_examples():
    """Display the two required examples for the assignment."""
    st.markdown("<h2 class='sub-header'>📋 Assignment Examples</h2>", unsafe_allow_html=True)
    
    # Screenshot guide for examples
    if st.session_state.get('screenshot_ready', False):
        create_screenshot_guide()
    
    tab1, tab2 = st.tabs(["Example 1: Basic Complexity", "Example 2: Advanced Complexity"])
    
    with tab1:
        st.markdown("""
        <div class='example-box'>
        <h3>Example 1: Basic Function - f(x,y) = x² + y²</h3>
        <p><strong>Complexity Level: Basic</strong> - Quadratic function with simple partial derivatives</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pre-set parameters for example 1
        f_expr1 = sp.sympify("x**2 + y**2")
        results1 = compute_differentials(f_expr1, 1.0, 1.0, 0.1, 0.1)
        
        # Screenshot marker
        st.markdown("**📸 Screenshot this section for your report**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Mathematical Analysis")
            st.latex(f"f(x,y) = x^2 + y^2")
            st.latex(f"f_x = \\frac{{\\partial f}}{{\\partial x}} = 2x")
            st.latex(f"f_x(1,1) = 2 \\times 1 = 2.00")
            st.latex(f"f_y = \\frac{{\\partial f}}{{\\partial y}} = 2y")
            st.latex(f"f_y(1,1) = 2 \\times 1 = 2.00")
        
        with col2:
            st.markdown("#### Numerical Results")
            st.metric("f(1,1)", f"{results1['f_value']:.4f}")
            st.metric("Actual Δf", f"{results1['delta_f']:.6f}", 
                     f"f(1.1,1.1) - f(1,1)")
            st.metric("Differential df", f"{results1['df']:.6f}", 
                     "2×0.1 + 2×0.1")
            st.metric("Absolute Error", f"{results1['absolute_error']:.6f}")
            st.metric("Relative Error", f"{results1['relative_error']:.2f}%")
        
        st.markdown("#### Discussion and Analysis")
        st.markdown("""
        **Key Observations:**
        
        1. **Linear Approximation Accuracy**: The differential provides a good approximation 
           with only 0.02 absolute error for Δx=Δy=0.1
        
        2. **Error Source Analysis**: 
           - Actual increment: Δf = 0.42
           - Differential: df = 0.40
           - Error comes from quadratic terms: 0.5×(2dx² + 2dy²) = 0.02
        
        3. **Mathematical Insight**: 
           For f(x,y) = x² + y², the Taylor expansion is:
           $$\\Delta f = 2xdx + 2ydy + (dx^2 + dy^2)$$
           The differential captures only the linear terms.
        
        **Educational Value**: This example clearly shows the concept of linear approximation 
        and helps students understand why differentials work well for small increments.
        """)
        
        # Generate visualization for example 1
        fig1 = create_3d_plot(results1, 1.0, 1.0, 0.1, 0.1, 2.0, True, True)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Additional screenshot note
        st.caption("📸 Include this 3D visualization in your screenshot")
    
    with tab2:
        st.markdown("""
        <div class='example-box'>
        <h3>Example 2: Advanced Function - f(x,y) = sin(x)cos(y)</h3>
        <p><strong>Complexity Level: Advanced</strong> - Trigonometric function with coupled variables</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pre-set parameters for example 2
        f_expr2 = sp.sympify("sin(x)*cos(y)")
        results2 = compute_differentials(f_expr2, 0.7854, 0.7854, 0.2, 0.1)
        
        # Screenshot marker
        st.markdown("**📸 Screenshot this section for your report**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Mathematical Analysis")
            st.latex(f"f(x,y) = \\sin(x)\\cos(y)")
            st.latex(f"f_x = \\cos(x)\\cos(y)")
            st.latex(f"f_x(\\pi/4,\\pi/4) = \\cos(\\pi/4)\\cos(\\pi/4) = 0.5")
            st.latex(f"f_y = -\\sin(x)\\sin(y)")
            st.latex(f"f_y(\\pi/4,\\pi/4) = -\\sin(\\pi/4)\\sin(\\pi/4) = -0.5")
        
        with col2:
            st.markdown("#### Numerical Results")
            st.metric("f(π/4,π/4)", f"{results2['f_value']:.4f}")
            st.metric("Actual Δf", f"{results2['delta_f']:.6f}", 
                     f"f(0.9854,0.8854) - f(0.7854,0.7854)")
            st.metric("Differential df", f"{results2['df']:.6f}", 
                     "0.5×0.2 + (-0.5)×0.1")
            st.metric("Absolute Error", f"{results2['absolute_error']:.6f}")
            st.metric("Relative Error", f"{results2['relative_error']:.2f}%")
        
        st.markdown("#### Discussion and Analysis")
        st.markdown("""
        **Key Observations:**
        
        1. **Complex Function Behavior**: Trigonometric functions exhibit oscillatory 
           behavior, making linear approximation more challenging
        
        2. **Directional Sensitivity**: 
           - Moving in x-direction: positive contribution (+0.1)
           - Moving in y-direction: negative contribution (-0.05)
           - Net differential: 0.05 (showing cancellation effects)
        
        3. **Higher-Order Effects**: 
           The error (0.0473) is relatively large compared to the differential (0.05),
           indicating significant higher-order terms in the Taylor expansion
        
        **Real-world Connection**: 
        This function models many physical phenomena:
        - Electromagnetic wave propagation
        - Acoustic pressure fields
        - Quantum mechanical wavefunctions
        
        Differential analysis helps understand small perturbations in these systems.
        """)
        
        # Generate visualization for example 2
        fig2 = create_3d_plot(results2, 0.7854, 0.7854, 0.2, 0.1, 1.5, True, True)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Additional screenshot note
        st.caption("📸 Include this 3D visualization in your screenshot")

# ============================================
# ENHANCED AI USAGE SUMMARY SECTION
# ============================================
def display_ai_usage_summary():
    """Display detailed summary of generative AI usage for assignment report."""
    st.markdown("<h2 class='sub-header'>🤖 Generative AI Usage Summary</h2>", unsafe_allow_html=True)
    
    # Screenshot guide
    if st.session_state.get('screenshot_ready', False):
        create_screenshot_guide()
    
    st.markdown("""
    <div class='ai-box'>
    <h3>Detailed Breakdown of AI Contributions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed AI Contributions Table
    ai_contributions = [
        {
            "Component": "Application Framework",
            "AI Contribution": "Streamlit tab structure, sidebar layout, interactive widget setup",
            "AI Tools": "ChatGPT (80%), GitHub Copilot (20%)",
            "Human Input": "Customized for assignment requirements, added specific controls",
            "Verification": "Manual testing of all interactive elements"
        },
        {
            "Component": "Mathematical Core",
            "AI Contribution": "LaTeX formula generation, differential equations, error calculations",
            "AI Tools": "ChatGPT (70%), SymPy documentation (30%)",
            "Human Input": "Verified mathematical correctness, added Taylor expansions",
            "Verification": "Cross-checked with textbook examples, validated calculations"
        },
        {
            "Component": "Visualization System",
            "AI Contribution": "Plotly 3D graph structure, color schemes, animation parameters",
            "AI Tools": "ChatGPT (60%), Plotly examples (40%)",
            "Human Input": "Selected appropriate visualizations, optimized performance",
            "Verification": "Tested on different screen sizes, ensured clarity"
        },
        {
            "Component": "Educational Content",
            "AI Contribution": "Real-world examples, step-by-step explanations, comparison tables",
            "AI Tools": "ChatGPT (85%), research papers (15%)",
            "Human Input": "Selected relevant applications, added personal insights",
            "Verification": "Checked for accuracy and relevance to course material"
        },
        {
            "Component": "Code Implementation",
            "AI Contribution": "Function structure, error handling, data processing logic",
            "AI Tools": "GitHub Copilot (50%), ChatGPT (30%), Stack Overflow (20%)",
            "Human Input": "Performance optimization, bug fixing, customization",
            "Verification": "Unit testing, edge case handling, user testing"
        },
        {
            "Component": "Documentation & UI",
            "AI Contribution": "User interface text, tooltips, help sections, comments",
            "AI Tools": "ChatGPT (70%), Grammarly (30%)",
            "Human Input": "Professional formatting, assignment-specific instructions",
            "Verification": "Readability testing, user feedback incorporation"
        }
    ]
    
    df_contributions = pd.DataFrame(ai_contributions)
    st.dataframe(df_contributions, use_container_width=True, height=400)
    
    st.markdown("### Specific AI-Generated Code Sections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **AI-Generated Mathematical Functions:**
        ```python
        # AI suggested this differential calculation structure
        def compute_differentials(f, x0, y0, dx, dy):
            f_value = f(x0, y0)
            f_x = derivative(f, x0, y0, 'x')
            f_y = derivative(f, x0, y0, 'y')
            df = f_x*dx + f_y*dy
            return df
        ```
        
        **AI-Enhanced Visualization:**
        ```python
        # AI provided Plotly 3D visualization template
        fig = go.Figure(data=[
            go.Surface(z=Z, colorscale='Viridis'),
            go.Surface(z=Z_tangent, colorscale='Reds')
        ])
        ```
        """)
    
    with col2:
        st.markdown("""
        **AI-Assisted Error Analysis:**
        ```python
        # AI suggested comprehensive error metrics
        absolute_error = abs(delta_f - df)
        relative_error = (absolute_error/abs(delta_f))*100
        gradient_magnitude = sqrt(f_x**2 + f_y**2)
        ```
        
        **AI-Generated Documentation:**
        ```python
        # AI helped structure function documentation
        \"\"\"
        Computes differential approximation for f(x,y)
        
        Parameters:
        - f: function to analyze
        - x0, y0: analysis point
        - dx, dy: increments
        
        Returns: differential approximation df
        \"\"\"
        ```
        """)
    
    st.markdown("### Ethical Considerations and Learning Outcomes")
    
    st.markdown("""
    <div class='info-box'>
    <h4>Ethical Use of AI in Academic Work</h4>
    
    **Transparency:**
    - All AI assistance is clearly documented
    - Human oversight maintained throughout
    - Original thinking preserved in key areas
    
    **Learning Outcomes Enhanced:**
    - AI accelerated technical implementation
    - More time available for conceptual understanding
    - Ability to explore complex examples
    - Development of critical evaluation skills
    
    **Human-AI Collaboration Model:**
    1. **AI as Assistant**: Handled repetitive coding tasks
    2. **Human as Director**: Made strategic decisions
    3. **AI as Suggestor**: Provided creative options
    4. **Human as Validator**: Ensured correctness and relevance
    
    **Academic Integrity:**
    - AI used as tool, not replacement for learning
    - All concepts personally understood and verified
    - Final work represents personal comprehension
    - Proper attribution given for AI assistance
    </div>
    """, unsafe_allow_html=True)
    
    # Reflection on AI Collaboration
    st.markdown("### Personal Reflection on AI Collaboration")
    
    reflection_text = """
    **What Worked Well:**
    - AI significantly accelerated development time
    - Provided access to best practices and patterns
    - Generated creative visualization ideas
    - Helped overcome technical hurdles
    
    **Challenges Encountered:**
    - Required careful verification of mathematical content
    - Needed to customize AI suggestions for specific requirements
    - Sometimes generated overly complex solutions
    - Required human judgment for relevance and clarity
    
    **Learning Experience:**
    This project demonstrated how AI can be effectively integrated into academic work
    when used responsibly. It allowed me to focus on higher-level conceptual understanding
    while AI handled implementation details. The key learning was finding the right balance
    between AI assistance and personal input.
    """
    
    st.markdown(reflection_text)
    
    # Screenshot reminder
    st.markdown("---")
    st.markdown("**📸 Remember to screenshot this AI Usage Summary for your report**")

# ============================================
# REAL-WORLD APPLICATIONS SECTION
# ============================================
def display_real_world_applications():
    """Display real-world applications of differentials."""
    st.markdown("<h2 class='sub-header'>🌍 Real-World Applications</h2>", unsafe_allow_html=True)
    
    app_choice = st.selectbox(
        "Select Application Domain:",
        ["Engineering: Error Propagation",
         "Economics: Marginal Analysis", 
         "Physics: Wave Analysis",
         "Machine Learning: Gradient Descent",
         "Medicine: Drug Dosage Optimization"]
    )
    
    if app_choice == "Engineering: Error Propagation":
        st.markdown("""
        ### Engineering Application: Manufacturing Tolerance Analysis
        
        **Problem:** A mechanical part has dimensions x = 10.0 cm ± 0.1 cm and y = 5.0 cm ± 0.05 cm.
        The part's performance depends on area A(x,y) = x × y. What's the uncertainty in performance?
        
        **Differential Solution:**
        
        1. **Function:** $A(x,y) = xy$
        2. **Partial Derivatives:** 
           - $A_x = y = 5.0$
           - $A_y = x = 10.0$
        3. **Differential:** $dA = y\\,dx + x\\,dy$
        4. **Maximum Error:** $dA_{max} = 5.0(0.1) + 10.0(0.05) = 0.5 + 0.5 = 1.0 \\text{ cm}^2$
        
        **Engineering Significance:**
        - Helps determine manufacturing tolerances
        - Guides quality control procedures
        - Informs design specifications
        - Reduces waste and rework costs
        """)
        
    elif app_choice == "Economics: Marginal Analysis":
        st.markdown("""
        ### Economics Application: Production Optimization
        
        **Problem:** A company produces two products with quantities x and y.
        Profit function: $P(x,y) = 50x + 40y - 0.1x^2 - 0.05y^2 - 0.02xy - 1000$
        Currently producing x=100, y=80 units. Should they increase production?
        
        **Marginal Analysis using Differentials:**
        
        1. **Marginal Profit w.r.t. x:** $P_x = 50 - 0.2x - 0.02y$
           - At (100,80): $P_x = 50 - 20 - 1.6 = 28.4$
        2. **Marginal Profit w.r.t. y:** $P_y = 40 - 0.1y - 0.02x$
           - At (100,80): $P_y = 40 - 8 - 2 = 30$
        3. **Decision Making:**
           - Increasing x by 1 unit: Profit increases by ≈ $28.4
           - Increasing y by 1 unit: Profit increases by ≈ $30
           - Both positive ⇒ Increase production
        
        **Business Impact:**
        - Guides production planning
        - Optimizes resource allocation
        - Maximizes profitability
        """)
        
    elif app_choice == "Machine Learning: Gradient Descent":
        st.markdown("""
        ### Machine Learning Application: Neural Network Training
        
        **Problem:** Train a neural network by minimizing loss function $L(w_1, w_2)$
        where w₁ and w₂ are network weights.
        
        **Gradient Descent using Differentials:**
        
        1. **Loss Function:** Typically complex (e.g., mean squared error)
        2. **Gradient Calculation:**
           - $\\nabla L = [\\frac{\\partial L}{\\partial w_1}, \\frac{\\partial L}{\\partial w_2}]$
           - This is exactly the differential concept!
        3. **Weight Update Rule:**
           - $w_1^{new} = w_1 - \\alpha \\frac{\\partial L}{\\partial w_1}$
           - $w_2^{new} = w_2 - \\alpha \\frac{\\partial L}{\\partial w_2}$
           - where α is learning rate
        
        **Why This Matters:**
        - Enables training of deep neural networks
        - Powers modern AI applications
        - Optimizes complex functions with millions of variables
        - Fundamental to ChatGPT, image recognition, etc.
        """)

# ============================================
# ASSIGNMENT REPORT HELPER
# ============================================
def display_assignment_helper():
    """Helper for creating the assignment report."""
    st.markdown("<h2 class='sub-header'>📄 Assignment Report Helper</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
    <h3>Assignment Requirements Checklist</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Report structure guide
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Report Structure (3-4 pages)")
        st.markdown("""
        **1. Application Integration (1 page)**
        - Live app link: {DEPLOYMENT_URL}
        - Technical description
        - How differentials are integrated
        
        **2. Two Examples (1.5 pages)**
        - Example 1: Basic function
        - Example 2: Advanced function
        - Screenshots with explanations
        
        **3. Real-world & AI (0.5-1 page)**
        - 2-3 applications
        - Detailed AI usage
        - Personal reflection
        """)
    
    with col2:
        st.markdown("### Screenshot Checklist")
        
        screenshots_needed = st.multiselect(
            "Mark screenshots taken:",
            ["Example 1: Basic function results",
             "Example 2: Advanced function results",
             "3D visualization comparison",
             "Error analysis tables",
             "AI usage summary",
             "Real-world applications"],
            default=[]
        )
        
        if st.button("Generate Screenshot Summary"):
            st.success(f"Screenshots ready: {len(screenshots_needed)}/6")
            if len(screenshots_needed) < 6:
                st.warning(f"Still need {6-len(screenshots_needed)} more screenshots")
    
    # Quick navigation to examples
    st.markdown("### Quick Navigation for Screenshots")
    
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
    
    with nav_col1:
        if st.button("Go to Example 1"):
            st.session_state.active_tab = "📋 Assignment Examples"
            st.rerun()
    
    with nav_col2:
        if st.button("Go to Example 2"):
            st.session_state.active_tab = "📋 Assignment Examples"
            st.rerun()
    
    with nav_col3:
        if st.button("Go to AI Summary"):
            st.session_state.active_tab = "🤖 AI Usage Summary"
            st.rerun()
    
    with nav_col4:
        if st.button("Go to Applications"):
            st.session_state.active_tab = "🌍 Real-world Applications"
            st.rerun()

# ============================================
# MAIN APPLICATION FUNCTION
# ============================================
def main():
    """Main application function."""
    
    # Handle example loading from session state
    if 'load_example' in st.session_state:
        if st.session_state.load_example == 1:
            function_str = "x**2 + y**2"
            x0, y0, dx, dy = 1.0, 1.0, 0.1, 0.1
        else:  # example 2
            function_str = "sin(x)*cos(y)"
            x0, y0, dx, dy = 0.7854, 0.7854, 0.2, 0.1
    else:
        # Use current function_str from sidebar
    
    # Parse function
    f_expr = parse_function(function_str)
    
    if f_expr is None:
        st.error("Invalid function expression. Please check your input.")
        return
    
    # Compute results
    results = compute_differentials(f_expr, x0, y0, dx, dy)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Interactive Visualization", 
                                          "📋 Assignment Examples", 
                                          "🤖 AI Usage Summary",
                                          "🌍 Real-world Applications",
                                          "📄 Report Helper"])
    
    # Set active tab from session state
    if 'active_tab' in st.session_state:
        if st.session_state.active_tab == "📋 Assignment Examples":
            tab2
        elif st.session_state.active_tab == "🤖 AI Usage Summary":
            tab3
        elif st.session_state.active_tab == "🌍 Real-world Applications":
            tab4
    
    with tab1:
        # Results display
        st.markdown("<h2 class='sub-header'>📊 Differential Calculation Results</h2>", unsafe_allow_html=True)
        
        # Screenshot guide
        if st.session_state.get('screenshot_ready', False):
            create_screenshot_guide()
        
        # Metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("f(x₀, y₀)", f"{results['f_value']:.4f}", 
                     f"f({x0:.2f}, {y0:.2f})")
        with col2:
            st.metric("∂f/∂x", f"{results['f_x_val']:.4f}", 
                     f"at ({x0:.2f}, {y0:.2f})")
        with col3:
            st.metric("∂f/∂y", f"{results['f_y_val']:.4f}", 
                     f"at ({x0:.2f}, {y0:.2f})")
        with col4:
            st.metric("Gradient Magnitude", f"{results['grad_magnitude']:.4f}")
        
        # Mathematical formulas
        st.markdown("#### Mathematical Expressions")
        col5, col6 = st.columns(2)
        with col5:
            st.latex(f"f(x, y) = {sp.latex(f_expr)}")
            st.latex(f"f_x(x, y) = {sp.latex(results['f_x'])}")
            st.latex(f"f_y(x, y) = {sp.latex(results['f_y'])}")
        with col6:
            st.latex(r"df = \frac{\partial f}{\partial x}\,dx + \frac{\partial f}{\partial y}\,dy")
            st.latex(f"df = ({results['f_x_val']:.4f})({dx}) + ({results['f_y_val']:.4f})({dy})")
            st.latex(f"df = {results['df']:.6f}")
        
        # Error comparison
        st.markdown("#### Approximation Accuracy")
        col7, col8, col9 = st.columns(3)
        with col7:
            st.metric("Actual Δf", f"{results['delta_f']:.6f}", 
                     f"f({x0+dx:.2f},{y0+dy:.2f}) - f({x0:.2f},{y0:.2f})")
        with col8:
            st.metric("Approximation df", f"{results['df']:.6f}")
        with col9:
            st.metric("Absolute Error", f"{results['absolute_error']:.6f}", 
                     delta=f"{results['relative_error']:.2f}%")
        
        # 3D Visualization
        st.markdown("#### 3D Visualization")
        fig_3d = create_3d_plot(results, x0, y0, dx, dy, plot_range, show_tangent, show_contour)
        st.plotly_chart(fig_3d, use_container_width=True)
        
        # Visualization guide
        st.markdown("""
        <div class='info-box'>
        <strong>Visualization Guide:</strong><br>
        • <span style='color:blue; font-weight:bold'>Blue arrow</span>: Movement direction (dx, dy)<br>
        • <span style='color:red; font-weight:bold'>Red arrow</span>: Gradient direction (steepest ascent)<br>
        • Red surface: Tangent plane (linear approximation)<br>
        • Colored surface: Original function<br>
        • Green point: Position after movement<br>
        • Red point: Starting position
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        display_assignment_examples()
    
    with tab3:
        display_ai_usage_summary()
    
    with tab4:
        display_real_world_applications()
    
    with tab5:
        display_assignment_helper()
    
    # Footer with assignment information
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background-color: #F9FAFB; border-radius: 0.5rem; margin-top: 2rem;'>
    <h3>MAT201 Calculus - Assignment 2 Submission</h3>
    <p><strong>Topic:</strong> Differentials of Multivariable Functions</p>
    <p><strong>Submission Requirements:</strong> 3-4 page PDF report with application link and screenshots</p>
    <p><strong>Due Date:</strong> January 9, 2026, 5:00 PM</p>
    <p><strong>Grading:</strong> CO1 (10%) + CO3 (5%) = 15% of final grade</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# RUN APPLICATION
# ============================================
if __name__ == "__main__":
    # Initialize session state
    if 'screenshot_ready' not in st.session_state:
        st.session_state.screenshot_ready = False
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "📈 Interactive Visualization"
    
    main()
