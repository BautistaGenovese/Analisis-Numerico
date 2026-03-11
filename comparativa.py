import streamlit as st
import grafico
import utils as ec
import pandas as pd
import biseccion, secante

def comparar_sec_bis(formula, inf, sup, err):
    col1, col2 = st.columns(2)
    with col1:
        raiz_bis, datos_bis = biseccion.biseccion(formula,inf,sup,err)
        st.title('Biseccion')
        st.success(f'Raíz encontrada en: $$x ≈ {round(raiz_bis,6)}$$')
        grafico.dibujar(formula, raiz_bis, inf, sup, key="grafico_biseccion")
        st.dataframe(pd.DataFrame(datos_bis))
        
    with col2:
        raiz_sec, datos_sec = secante.secante(formula,inf,sup,err)
        st.title('Secante')
        st.success(f'Raíz encontrada en: $$x ≈ {round(raiz_sec,6)}$$')
        grafico.dibujar(formula, raiz_sec, inf, sup, key="grafico_secante")
        st.dataframe(pd.DataFrame(datos_sec))