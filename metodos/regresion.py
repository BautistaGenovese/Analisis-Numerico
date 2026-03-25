import streamlit as st, pandas as pd
from core import algoritmos, grafico, utils as ut

def mostrar_info():
    st.markdown("<h1 style='text-align: center;'>Regresión Lineal</h1>", unsafe_allow_html=True)
    
    with st.expander("📖 ¿Cómo funciona la Regresión Lineal?"):
        st.markdown("""
        **Concepto básico:** A diferencia de los métodos anteriores, aquí no buscamos la raíz de una ecuación no lineal, sino que modelamos la relación entre un conjunto de datos (puntos sueltos). La regresión lineal simple busca la **recta de mejor ajuste** que minimice la distancia vertical (error cuadrático) entre los puntos reales y la recta trazada.
        
        **Ecuación de la recta resultante:**
        """)
        st.latex(r"f(x) = mx + b")
        
        st.markdown("""
        Donde:
        * **$m$**: Pendiente de la recta.
        * **$b$**: Ordenada al origen (intersección con el eje Y).
        
        **Intervalos permitidos y Condiciones:**
        * Se requiere ingresar como mínimo **dos pares de coordenadas** $(x, y)$.
        * El cálculo de la raíz (donde la recta cruza el eje X) se realiza despejando la ecuación resultante, siempre y cuando la pendiente $m$ no sea exactamente cero.
        """)
    
    with st.container(border=True):
            col_in, col_out = st.columns([1, 2], gap="large")

            with col_in:
                st.subheader("📥 Ingreso de datos")
                st.info("💡 Edita la tabla directamente. Toca la fila vacía al final para agregar más puntos.")
                
                # 1. Creamos una tablita por defecto
                df_base = pd.DataFrame({
                    "x": [1.0, 2.0, 3.0], 
                    "y": [2.1, 4.0, 6.2]
                })
                
                # 2. LA MAGIA: Editor de datos interactivo (Reemplaza al session_state)
                df_usuario = st.data_editor(
                    df_base, 
                    num_rows="dynamic", # Permite agregar o borrar filas
                    use_container_width=True,
                    key="editor_regresion"
                )
                
                # 3. Extraemos los datos crudos de la tablita a listas normales de Python
                x_vals = df_usuario["x"].dropna().tolist()
                y_vals = df_usuario["y"].dropna().tolist()


                # Realizamos el cálculo
                m, b, raiz, r2 = algoritmos.calcular_regresion(x_vals, y_vals)
                
                if m is not None:
                    st.subheader('📈 Función')
                    
                    inf_grafico = min(raiz, min(x_vals)) - 1
                    sup_grafico = max(raiz, max(x_vals)) + 1
                    formula_str = f"{m}*x + {b}"
                    datos_dict = {'x': x_vals, 'y': y_vals}
                    
                    with st.spinner('Generando gráfica...'):
                        fig = grafico.obtener_grafico(
                                f=formula_str, 
                                raiz=raiz, 
                                inf=inf_grafico, 
                                sup=sup_grafico, 
                                key='regresion', 
                                iteraciones=datos_dict
                                ) 
                    st.latex(f'f(x) = {m:.4f}x {"+" if b>=0 else "-"} {abs(b):.4f}')
                    st.divider()
                    
                    ut.boton_descarga(
                        metodo='Regresión',
                        formula=f'{m:.4f}x {"+" if b>=0 else "-"} {abs(b):.4f}',
                        parametros=f"Pendiente (m): {m:.4f}, Ordenada (b): {b:.4f}, (R²): {r2:.4f}",
                        raiz=raiz,
                        datos=datos_dict,
                        fig=fig
                        )
                    

            with col_out:
                st.space('small')
                # Mostramos resultados si hay datos válidos
                if m is not None and raiz is not None:
                    st.success(f'Raíz (Intersección con X) encontrada en: $x \\approx {raiz:.6f}$')
                    
                    # Dibujamos
                    grafico.dibujar(fig)
                    
                    # Panel de métricas en lugar de tabla de iteraciones
                    with st.expander("📊 Ver métricas del modelo"):
                        st.write(f"- **Pendiente ($m$):** `{m:.4f}`")
                        st.write(f"- **Ordenada al origen ($b$):** `{b:.4f}`")
                        st.write(f"- **Coeficiente de determinación ($R^2$):** `{r2:.4f}` (Mide qué tan bien se ajusta la recta)")
                        
                else:
                    st.warning('Agrega al menos 2 puntos válidos con una pendiente distinta de cero para calcular la regresión.')
                    
    st.divider()
    st.header('Código hecho en Python')
    st.code('''
def calcular_regresion(datos):
    m, int = statistics.linear_regression(
        datos['x'],
        datos['y']
    )
    if m != 0:
        raiz = int / m * (-1)
        return m, int, raiz
        
    else:
        st.error('La recta no tiene raices.')
        return None
            ''',
            "python")

    