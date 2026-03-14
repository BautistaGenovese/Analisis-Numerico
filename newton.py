import sympy as sp
import numpy as np
import re
import utils as ec
import streamlit as st
import comparativa, grafico
import pandas as pd
import base64
import streamlit.components.v1 as components

def newton(x_n,f,err):
   # Creamos el diccionario para guardar las iteraciones
    cuadro = {
        'x[i]': [],
        'f(x[i])': [],
        "f'(x[i])": [],
        'x[i+1]': []
    }
    
    while True:
        fa = ec.evaluar_f(f, x_n)
        derivada = str(sp.diff(f, 'x'))
        d_evaluada = round(ec.evaluar_f(derivada, x_n), 6)
        
        # Evitamos la división por cero si la derivada da 0
        if d_evaluada == 0:
            return None, cuadro
            
        x_n1 = round(x_n - fa / d_evaluada, 6)

        # Guardamos los datos de esta vuelta en el cuadro
        cuadro['x[i]'].append(x_n)
        cuadro['f(x[i])'].append(fa)
        cuadro["f'(x[i])"].append(d_evaluada)
        cuadro['x[i+1]'].append(x_n1)

        # Condición de corte
        if abs(ec.evaluar_f(f, x_n1)) <= err:
            return x_n1, cuadro
        
        # Condición de corte por si se estanca
        if x_n == x_n1:
            return x_n1, cuadro
        
        x_n = x_n1

def mostrar_info():
    st.header('Metodo de Newton')
    # Dividimos la pantalla: 1 parte para inputs, 2 partes para gráficos
    col_in, col_out = st.columns([1, 2], gap="large")

    with col_in:
        formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
        st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")
        st.latex(ec.mostrar_formula(formula))
        c1, c2 = st.columns(2)
        with c1:
            x_n = st.number_input('Ingresar valor inicial $x_n$',value=-10.0,step=2.0)
        with c2:
            err = st.number_input('Tolerancia de error $E = 10^{-n}$',value=2,min_value=1, max_value=10)
            err = 10**(-err)
    
        try:
            raiz, datos = newton(x_n, formula, err)
            if raiz is not None:
                # Pastillitas de selección única para comparar
                seleccion = st.pills(
                    label="Comparar con:", 
                    options=["Bisección", "Secante"], 
                    key="pills_newton", 
                    selection_mode='single'
                )
                
                mostrar_datos = st.checkbox("Mostrar iteraciones en el gráfico")
                # Si eligió alguna de las opciones
                if seleccion:
                    st.info(f"Para comparar con {seleccion}, necesitamos un intervalo inicial:")
                    col1, col2 = st.columns(2)
                    with col1:
                        inf = st.number_input('Ingresar intervalo inferior', value=x_n - 5.0, step=1.0)
                    with col2:
                        sup = st.number_input('Ingresar intervalo superior', value=x_n + 5.0, step=1.0)
                
        except Exception as e:
            raiz = None
            st.error(f'Error en la fórmula: {e}')
            st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')
    with col_out:
        # Si no eligió nada, muestra solo Newton
        if 'raiz' in locals() and raiz is not None:
            if seleccion == None:
                st.space('small')
                st.success(f'Raíz encontrada en: $$x \\approx {round(raiz,6)}$$')
                inf_grafico = raiz - 5
                sup_grafico = raiz + 5
                grafico.dibujar(formula, raiz, inf_grafico, sup_grafico, key="graf_unico_newton", iteraciones=datos if mostrar_datos else None)
            else:
                comparativa.comparar_generico("Newton", seleccion, formula, err, mostrar_datos, x_n=x_n, inf=inf, sup=sup)

                # Expander para la tabla
                with st.expander("Ver tabla de iteraciones"):
                    st.dataframe(pd.DataFrame(datos), use_container_width=True)        
        else:
            if 'raiz' in locals():
                st.error('No se ha encontrado la raíz o no hay cambio de signo en el intervalo.')



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
