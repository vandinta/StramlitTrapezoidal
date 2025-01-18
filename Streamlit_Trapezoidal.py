import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, lambdify, symbols, integrate

st.title("Integrasi Metode Numerik Dengan Metode Trapezoidal Rule")
st.write("Aplikasi ini menunjukkan Aturan Trapesium untuk integrasi numerik. Anda dapat memasukkan fungsi, menentukan batas integrasi, dan mengamati hasilnya.")

function_input = st.text_input("Masukkan fungsi yang akan diintegrasikan (dalam bentuk x) :", value="sin(x)")

try:
    func_expr = sympify(function_input)
    x = symbols('x')
    func = lambdify(x, func_expr, 'numpy')
except Exception as e:
    st.error(f"Function Tidak Sesuai : {e}")
    st.stop()

a = st.number_input("Batas bawah integrasi (a) :", value=2.0)
b = st.number_input("Batas atas integrasi (b) :", value=14.0)
n = st.slider("Number of sub-intervals (n):", min_value=1, max_value=100, value=24)

if a >= b:
    st.error("Batas bawah (a) harus lebih kecil dari batas atas (b).")
    st.stop()

def trapezoidal_rule(func, a, b, n):
    x_vals = np.linspace(a, b, n + 1)
    y_vals = func(x_vals)
    h = (b - a) / n
    integral = h * (0.5 * y_vals[0] + 0.5 * y_vals[-1] + np.sum(y_vals[1:-1]))
    return integral, x_vals, y_vals

numerical_integral, x_vals, y_vals = trapezoidal_rule(func, a, b, n)

try:
    exact_integral = float(integrate(func_expr, (x, a, b)))
except Exception:
    exact_integral = None

st.subheader("Hasil Trapezoidal Rule")
st.write(f"Integral Numerik (Trapezoidal Rule) : {numerical_integral:.6f}")
if exact_integral is not None:
    st.write(f"Integral Tepat : {exact_integral:.6f}")
    st.write(f"Error: {abs(numerical_integral - exact_integral):.6f}")
else:
    st.write("Integral eksak tidak dapat dihitung.")

# Plot
fig, ax = plt.subplots()
ax.plot(x_vals, y_vals, 'o-', label="Function")
for i in range(n):
    ax.fill_between([x_vals[i], x_vals[i+1]], [y_vals[i], y_vals[i+1]], color='blue', alpha=0.5)
ax.set_title("Pendekatan Trapesium")
ax.legend()
ax.grid(True)
st.pyplot(fig)