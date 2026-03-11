import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import utils as ec
import pandas as pd

def secante(f,a,b,err):
    cuadro = {
    'a[i]':[],
    'b[i]':[],
    'x[i]':[],
    'f(x[i])':[],
    'Dx[i]':[]
    }
    fa = ec.evaluar_f(f,a)
    fb = ec.evaluar_f(f,b)

    # Casos base
    if fa * fb > 0:
        return None, []
    if a  > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Calculo de la raíz
    """for _ in range(1, max_i+1):
        x = b - (fb * (b-a))/(fb - fa)
        fx = ec.evaluar_f(f,x)"""
    valor_anterior= a
    while True :
        
        x = b - (fb * (b - a)) / (fb - fa)
        fx = ec.evaluar_f(f, x)

        if round(x,6) == round(valor_anterior,6):
            break
        
        cuadro['a[i]'].append(a)
        cuadro['b[i]'].append(b)
        cuadro['x[i]'].append(x)
        cuadro['f(x[i])'].append(fx)
        cuadro['Dx[i]'].append(x-a)

        if abs(fx) < err: 
            return x, cuadro
        valor_anterior= x
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx

    return x, cuadro

def mostrar_info():
    st.header('Metodo Secante')
    
    formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
    st.caption("Usa `**` para potencias (ej: `x**2`) y `*` para productos. También puedes usar `sin(x)`, `exp(x)`, etc.")
    
    st.latex(ec.mostrar_formula(formula))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        inf = st.number_input('Ingresar intervalo inferior',value=-10.0,step=2.0)
    with col2:
        sup = st.number_input('Ingresar intervalo superior',value=10.0,step=2.0)
    with col3:
        err = st.number_input('Exponente de tolerancia de error',value=2,min_value=1, max_value=10)
        err = 10**(-err)
    try:
        x = np.linspace(inf, sup, 100)
        y = ec.evaluar_f(formula,x)
        
        fig, ax = plt.subplots()
        p_x, datos = secante(formula,inf,sup,err)
        
        if p_x is not None:
            ax.scatter(p_x,0.0,color='green', s=30, zorder=5, label="Punto aproximado")
            st.success(f'Raíz encontrada en: $$x ≈ {round(p_x,6)}$$')

            ax.plot(x, y, label='$f (x)$', color='skyblue', linewidth=2)
            ax.set_xlabel("Eje X")
            ax.set_ylabel("Eje Y")
            ax.legend()
            ax.grid(True)
            
            # Mostrar la figura en Streamlit
            st.pyplot(fig)

            mostrar_datos = st.checkbox("Mostrar datos de iteraciones")
            if mostrar_datos:
                st.dataframe(pd.DataFrame(datos))
        else:
            st.error('No se ha encontrado la raíz.')

    except Exception as e:
        st.error(f'Error en la fórmula: {e}')
        st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')

    st.divider()
    st.header('Código hecho en Python')
    st.code('''
def secante(f,a,b,err,max_i):
    fa = f(a)
    fb = f(b)
    # Casos base
    if f(a) * f(b) > 0:
        return None
    if a  > b:
        a, b = b, a
    # Calculo de la raíz
    while True :
        valor_anterior= b
        x = b - (fb * (b - a)) / (fb - fa)
        fx = ec.evaluar_f(f, x)

        if round(x,6) == round(valor_anterior,6):
            break''',
            "python")