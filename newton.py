import sympy as sp
import numpy as np
import re
import utils as ec
import streamlit as st
import comparativa, grafico
import pandas as pd

def newton(x_n,f,err):
    """cuadro = {
    'a[i]':[],
    'x[i]':[],
    'f(x[i])':[],
    'Dx[i]':[]
    }"""
    
    while True:
        fa=ec.evaluar_f(f,x_n)
        derivada=str(sp.diff(f, 'x'))
        d_evaluada= round(ec.evaluar_f(derivada,x_n),6)
        x_n1=round(x_n-fa/d_evaluada,6)

        if round(ec.evaluar_f(f,x_n1),6)<=err:
            return x_n1
        
        x_n=x_n1 


#print("ingrese el primer punto")
#a=input()
x_n=-1.0
#print("ingrese el error")
#err=float(input())
err=0.00001
#print("ingrese la formula")
#f=input()
f="(x-6)**2"

def mostrar_info():
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.pagina_actual = "Inicio"
        st.rerun()

    st.header('Metodo de Newton')

    formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
    st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")

    st.latex(ec.mostrar_formula(formula))

    col1, col2, col3 = st.columns(3)
    with col1:
        inf = st.number_input('Ingresar intervalo inferior',value=-10.0,step=2.0)
    with col2:
        sup = st.number_input('Ingresar intervalo superior',value=10.0,step=2.0)
    with col3:
        err = st.number_input('Tolerancia de error $E = 10^{-n}$',value=2,min_value=1, max_value=10)
        err = 10**(-err)
    try:
        raiz, datos = newton(x_n,f,err)

        if raiz is not None:
            comparar = st.checkbox("Comparar con Secante")
            if comparar:
                comparativa.comparar_sec_bis(formula,inf,sup,err)
            else:
                st.success(f'Raíz encontrada en: $$x ≈ {round(raiz,6)}$$')

                grafico.dibujar(formula, raiz, inf, sup,key="grafico_unico")
                    
                mostrar_datos = st.checkbox("Mostrar datos de iteraciones")
                
                if mostrar_datos:
                    st.dataframe(pd.DataFrame(datos), use_container_width=True)          
        else:
            st.error('No se ha encontrado la raíz o la derivada se hizo cero.')

    except Exception as e:
        st.error(f'Error en la fórmula: {e}')
        st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')


    st.divider()
    st.header('Código hecho en Python')
    st.code('''
def newton(x_n,f,err):
    
    while True:
        fa = ec.evaluar_f(f, x_n)
        derivada = str(sp.diff(f, 'x'))
        d_evaluada = round(ec.evaluar_f(derivada, x_n), 6)
        
        # Evitamos la división por cero si la derivada da 0
        if d_evaluada == 0:
            return None, cuadro
            
        x_n1 = round(x_n - fa / d_evaluada, 6)

        # Condición de corte
        if abs(ec.evaluar_f(f, x_n1)) <= err:
            return x_n1, cuadro
        
        # Condición de corte por si se estanca
        if x_n == x_n1:
            return x_n1, cuadro
        
        x_n = x_n1''',
            "python")




