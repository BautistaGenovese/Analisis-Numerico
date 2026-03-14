import streamlit as st
import pandas as pd
import grafico
import biseccion
import secante
import newton

def comparar_generico(nombre_metodo1, nombre_metodo2, formula, err, mostrar_datos, **kwargs):
    # Ya estamos dentro de col_out, así que estas columnas dividirán la mitad derecha en dos
    col1, col2 = st.columns(2)
    
    def ejecutar_metodo(nombre):
        if nombre == "Bisección":
            return biseccion.biseccion(formula, kwargs.get('inf'), kwargs.get('sup'), err)
        elif nombre == "Secante":
            return secante.secante(formula, kwargs.get('inf'), kwargs.get('sup'), err)
        elif nombre == "Newton":
            return newton.newton(kwargs.get('x_n'), formula, err)
        return None, []

    with col1:
        st.subheader(nombre_metodo1)
        raiz1, datos1 = ejecutar_metodo(nombre_metodo1)
        
        if raiz1 is not None:
            st.success(f'Raíz en: $x \\approx {round(raiz1,6)}$')     
            inf1 = kwargs.get('inf', raiz1 - 5)
            sup1 = kwargs.get('sup', raiz1 + 5)
            grafico.dibujar(formula, raiz1, inf1, sup1, key=f"graf_{nombre_metodo1}", iteraciones=datos1 if mostrar_datos else None)
            
            # Tabla dentro del expander
            with st.expander(f"Ver tabla - {nombre_metodo1}"):
                st.dataframe(pd.DataFrame(datos1), use_container_width=True)
        else:
            st.error("No convergió")

    with col2:
        st.subheader(nombre_metodo2)
        raiz2, datos2 = ejecutar_metodo(nombre_metodo2)
        
        if raiz2 is not None:
            st.success(f'Raíz en: $x \\approx {round(raiz2,6)}$')  
            inf2 = kwargs.get('inf', raiz2 - 5)
            sup2 = kwargs.get('sup', raiz2 + 5)
            grafico.dibujar(formula, raiz2, inf2, sup2, key=f"graf_{nombre_metodo2}", iteraciones=datos2 if mostrar_datos else None)
            
            # Tabla dentro del expander
            with st.expander(f"Ver tabla - {nombre_metodo2}"):
                st.dataframe(pd.DataFrame(datos2), use_container_width=True)
        else:
            st.error("No convergió")