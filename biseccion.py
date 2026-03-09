import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import ecuacion as ec
import pandas as pd

def biseccion(f,a,b,err,max_i):
    cuadro = {
    'a[i]':[],
    'b[i]':[],
    'x[i]':[],
    'f(x[i])':[]
    }
    fa = ec.evaluar_f(f,a)
    fb = ec.evaluar_f(f,b)

    # Casos base
    if fa * fb>0:
        return None, []
    if a  > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Calculo de la raíz
    for _ in range(1, max_i+1):
        x = (a+b)/2
        fx = ec.evaluar_f(f,x)

        cuadro['a[i]'].append(a)
        cuadro['b[i]'].append(b)
        cuadro['x[i]'].append(x)
        cuadro['f(x[i])'].append(fx)

        if abs(fx) < err or max_i<=0: 
            return x, cuadro
        
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx

    return x, cuadro

def mostrar_info():
    st.header('Metodo Bisección')
    
    formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
    st.caption("Usa `**` para potencias (ej: `x**2`) y `*` para productos. También puedes usar `sin(x)`, `exp(x)`, etc.")
    
    st.latex(ec.formateador_pro(formula))
    
    col1, col2 = st.columns(2)
    with col1:
        inf = st.number_input('Ingresar intervalo inferior',value=-10.0,step=0.5)
        sup = st.number_input('Ingresar intervalo superior',value=10.0,step=0.5)
    with col2:
        max_i = st.number_input('Ingresar cantidad de iteraciones',min_value=1,max_value=30,value=5)
        err = st.number_input('Exponente de tolerancia de error $E = 10^{-n}$',value=2,min_value=1, max_value=10)
        err = 10**(-err)
    try:
        x = np.linspace(inf, sup, 100)
        y = ec.evaluar_f(formula,x)
        
        fig, ax = plt.subplots()
        p_x, datos = biseccion(formula,inf,sup,err,max_i)
        
        if p_x is not None:
            ax.scatter(p_x,0.0,color='green', s=30, zorder=5, label="Punto aproximado")
            st.success(f'Raíz encontrada en: $$x ≈ {p_x}$$')
            # st.balloons()

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
def biseccion(f,a,b,err,max_i):
    fa = f(a)
    fb = f(b)
    # Casos base
    if f(a) * f(b) > 0:
        return None
    if a  > b:
        a, b = b, a
    # Calculo de la raíz
    for i in range(1, max_i+1):
        x = (a+b)/2
        fx = f(x)
        if abs(fx) < err or max_i<=0: 
            return x
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
    return x''',
            "python")