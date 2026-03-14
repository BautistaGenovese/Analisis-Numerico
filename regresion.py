import streamlit as st
import pandas as pd
import statistics
import grafico

def agregar_dato():
    # Usamos los valores actuales de los inputs
    st.session_state.datos['x'].append(st.session_state.input_x)
    st.session_state.datos['y'].append(st.session_state.input_y)
    # Limpiamos los inputs reseteando su estado
    st.session_state.input_x = 0.0
    st.session_state.input_y = 0.0

def calcular_regresión():
    m, int = statistics.linear_regression(
        st.session_state.datos['x'],
        st.session_state.datos['y']
    )
    if m != 0:
        raiz = int / m * (-1)
        return m, int, raiz
        

    else:
        st.error('La recta no tiene raices.')
        return None
    
def mostrar_info():
    st.header('Regresión Lineal')
    
    # Inicializamos el contenedor de datos si no existe
    if 'datos' not in st.session_state:
        st.session_state.datos = {'x': [], 'y': []}

    col1, col2 = st.columns(2)
    with col1:
        # La key maneja automáticamente el valor en session_state
        st.number_input('Ingresar $x$:', key='input_x', format="%.4f", step=1.0)
    with col2:
        st.number_input('Ingresar $y$:', key='input_y', format="%.4f", step=1.0)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.button('Agregar Dato', on_click=agregar_dato, use_container_width=True)
    with c2:
        if st.button('Borrar último', use_container_width=True):
            if st.session_state.datos['x']:
                st.session_state.datos['x'].pop()
                st.session_state.datos['y'].pop()
    with c3:
        if st.button('Borrar datos', use_container_width=True):
            if st.session_state.datos['x']:
                st.session_state.datos = {'x': [], 'y': []}

    st.dataframe(
        pd.DataFrame(st.session_state.datos),
        use_container_width=True,
        hide_index=True,
        key='puntos'
    )

    if len(st.session_state.datos['x']) > 1:
        m, int, raiz = calcular_regresión()
        st.latex(f'f(x) = {m:.4f}x {'+' if int>=0 else '-'} {abs(int):.4f}')

        grafico.dibujar(
            f=f'{m}x + {int}',
            raiz=raiz,
            inf=min(raiz,0),
            sup=max(raiz,0),
            key='regresion',
            iteraciones=st.session_state.datos
        )
        with st.expander("Mostrar datos de la regresión"):
            st.write(f'Raiz encontrada en $$x ≈ {raiz:.4f}$$')
            st.write(f'Pendiente $$m ≈ {m:.4f}$$')
            st.write(f'Intersección con el eje: $$y ≈ {int:.4f}$$')
            
        
    else:
        st.info('Debes de agregar por lo menos 2 puntos.')
    