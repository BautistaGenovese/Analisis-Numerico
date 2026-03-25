import streamlit as st
from core import algoritmos, grafico, utils as ut
import time

def renderizar_metodo(nombre_metodo, id_columna, formula, err):
    st.subheader(nombre_metodo)
    
    # Valores por defecto para que el gráfico no explote
    raiz, datos = None, None
    a_graf, b_graf = -10.0, 10.0
    tiempo_ejecucion_ms = 0.0
    
    try:
        
        inicio = time.perf_counter()
        
        if nombre_metodo == "Bisección":
            c_a, c_b = st.columns(2)
            with c_a: a = st.number_input('Límite inf $(a)$', value=0.0, key=f"a_{id_columna}")
            with c_b: b = st.number_input('Límite sup $(b)$', value=2.0, key=f"b_{id_columna}")
            
            raiz, datos = algoritmos.biseccion(formula, a, b, err)
            a_graf, b_graf = a, b
                
        elif nombre_metodo == "Secante":
            c_x0, c_x1 = st.columns(2)
            with c_x0: x0 = st.number_input('Punto $x_0$', value=0.0, key=f"x0_{id_columna}")
            with c_x1: x1 = st.number_input('Punto $x_1$', value=1.0, key=f"x1_{id_columna}")

            raiz, datos = algoritmos.secante(formula, x0, x1, err)
            a_graf, b_graf = x0, x1
                
        elif nombre_metodo == "Newton":
            x0 = st.number_input('Punto inicial $x_0$', value=0.0, key=f"n_x0_{id_columna}")

            raiz, datos = algoritmos.newton(x0, formula, err)
            if raiz is not None:
                a_graf, b_graf = raiz - 5, raiz + 5 
                
        elif nombre_metodo == "Punto Fijo":
            c1, c2 = st.columns(2)
            with c1: g_form = st.text_input('Función despejada $g(x)$:', value='(6 - x**2)/11', key=f"g_{id_columna}")
            with c2: x0 = st.number_input('Punto inicial $x_0$', value=0.0, key=f"pf_x0_{id_columna}")

            raiz, datos, converge = algoritmos.punto_fijo(g_form, x0, err)
            if not converge: 
                raiz = None # Si diverge, lo forzamos a None para que tire error abajo
            elif raiz is not None:
                a_graf, b_graf = raiz - 5, raiz + 5

        fin = time.perf_counter()
        
        tiempo_ejecucion_ms = (fin - inicio) * 1000
        
        # Renderizamos el resultado y el gráfico de f(x) de este método
        if raiz is not None:
            st.success(f'Raíz encontrada en: $x \\approx {round(raiz,6)}$')
            grafico_func = grafico.obtener_grafico(formula, raiz, a_graf, b_graf, key=f"graf_{id_columna}", iteraciones=datos.obtener_datos())
            grafico.dibujar(grafico_func)
        else:
            st.error('😥 No se ha encontrado la raíz o el método diverge.')

    except Exception as e:
        st.error('⚠️ Revisa los parámetros ingresados.')

    # Devolvemos todo para que la pantalla principal pueda armar la comparativa
    return raiz, datos, nombre_metodo, tiempo_ejecucion_ms

# === FUNCIÓN PRINCIPAL ===

def mostrar_info():
    st.markdown("<h2 style='text-align: center;'>Comparación de Métodos</h2>", unsafe_allow_html=True)
    
    # Datos Globales
    formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
    st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $e^{1-x}$.")
    st.latex(ut.mostrar_formula(formula))
    
    err_exp = st.slider('Precisión ($n$ en $10^{-n}$)', 1, 10, 2)
    err = 10**(-err_exp)

    # Selectores "VS"
    col1, col2, col3 = st.columns([2, 1, 2], gap="small")
    with col1:
        opc1 = st.selectbox('Rincón Azul:', key='opc1', index=None, options=["Bisección", "Secante", "Newton", "Punto Fijo"])
    with col2:
        st.markdown("<h2 style='text-align: center; font-weight:800; margin-top: 15px;'>VS</h2>", unsafe_allow_html=True)
    with col3:
        opc2 = st.selectbox('Rincón Rojo:', key='opc2', index=None, options=["Bisección", "Secante", "Newton", "Punto Fijo"])

    if opc1 is None or opc2 is None:
        st.info('🧮 Selecciona dos métodos en los menús de arriba para comenzar la batalla.')
    elif opc1 == opc2:
        st.warning('⚠️ Por favor, elige métodos distintos para poder compararlos.')
    else:
        st.divider()
        met1, met2 = st.columns(2, gap="large")
        
        with met1:
            raiz_1, datos_1, nom_1, tiempo_1 = renderizar_metodo(opc1, "izq", formula, err)
        with met2:
            raiz_2, datos_2, nom_2, tiempo_2 = renderizar_metodo(opc2, "der", formula, err)
        
        # === MÉTRICAS RÁPIDAS Y GRÁFICO FINAL ===
        if raiz_1 is not None and raiz_2 is not None:
            with st.expander("📊 Ver tablas detalladas de iteraciones"):
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    st.markdown(f"**{nom_1}**")
                    st.table(datos_1.obtener_dataframe())
                with col_t2:
                    st.markdown(f"**{nom_2}**")
                    st.table(datos_2.obtener_dataframe())
            st.divider()
            st.subheader("🏆 Resultados de la Comparación")
            
            # Recuperamos datos crudos
            d_izq = datos_1.obtener_datos()
            d_der = datos_2.obtener_datos()
            iters_1 = len(d_izq['x[i]'])
            iters_2 = len(d_der['x[i]'])

            costo_1 = 2 + iters_1 if nom_1 != "Newton" else 2 * iters_1
            costo_2 = 2 + iters_2 if nom_2 != "Newton" else 2 * iters_2
            
            # --- DISEÑO DE BATALLA (Limpio y Nativo) ---
            st.markdown("<br>", unsafe_allow_html=True) # Un espaciecito extra para que respire
            
            # Usamos 2 columnas simples, sin márgenes raros
            col_azul, col_rojo = st.columns(2, gap="large")

            with col_azul:
                st.markdown(f"<h3 style='color: #3498DB;'>🔵 {nom_1}</h3>", unsafe_allow_html=True)
                
                st.metric(label="Raíz encontrada", value=f"{raiz_1:.6f}")
                
                st.metric(
                    label="Iteraciones", 
                    value=iters_1, 
                    delta=f"{iters_1 - iters_2} pasos", 
                    delta_color="inverse"
                )
                
                st.metric(
                    label="Tiempo (ms)", 
                    value=f"{tiempo_1:.3f}", 
                    delta=f"{(tiempo_1 - tiempo_2):.3f} ms", 
                    delta_color="inverse"
                )
                
                st.metric(
                    label="Cálculos de f(x)", 
                    value=costo_1, 
                    delta=f"{costo_1 - costo_2} cálculos", 
                    delta_color="inverse"
                )

            with col_rojo:
                st.markdown(f"<h3 style='color: #E74C3C;'>🔴 {nom_2}</h3>", unsafe_allow_html=True)
                
                st.metric(label="Raíz encontrada", value=f"{raiz_2:.6f}")
                
                st.metric(
                    label="Iteraciones", 
                    value=iters_2, 
                    delta=f"{iters_2 - iters_1} pasos", 
                    delta_color="inverse"
                )
                
                st.metric(
                    label="Tiempo (ms)", 
                    value=f"{tiempo_2:.3f}", 
                    delta=f"{(tiempo_2 - tiempo_1):.3f} ms", 
                    delta_color="inverse"
                )
                
                st.metric(
                    label="Cálculos de f(x)", 
                    value=costo_2, 
                    delta=f"{costo_2 - costo_1} cálculos", 
                    delta_color="inverse"
                )
                
            grafico.dibujar_batalla_errores(
                datos_1.obtener_datos(), 
                datos_2.obtener_datos(), 
                nom_1, 
                nom_2
            )
            
            # === NUEVA ZONA DEL VEREDICTO FINAL ===
            st.write("#### Análisis Multi-Criterio")
            col_ver1, col_ver2 = st.columns([1, 2], gap="large")

            # --- A. Lógica de Puntuación (Normalización) ---
            # Para velocidad y costo, "menos" es "mejor". Queremos puntajes 0-10 donde 10 es "menos".
            # Usamos una normalización simple: (valor_min / valor_actual) * 10.
            
            # Categoría: VELOCIDAD (Tiempo o Iters)
            # Usamos tiempo de ejecución si lo mediste (ver Turn 22), o iters como respaldo.
            min_time = min(tiempo_1, tiempo_2)
            score_vel_izq = (min_time / tiempo_1) * 10
            score_vel_der = (min_time / tiempo_2) * 10

            # Categoría: COSTO (Evaluaciones Totales)
            min_cost = min(costo_1, costo_2)
            score_costo_izq = (min_cost / costo_1) * 10
            score_costo_der = (min_cost / costo_2) * 10

            # Categoría: ROBUSTEZ (Puntaje cualitativo conocido en Análisis Numérico)
            robustness_scores = {
                "Bisección": 10.0, # Garantizado
                "Secante": 6.5,    # Abierto, pero más estable
                "Newton": 4.0,     # Rápido pero diverge fácil (como viste con punto fijo automático)
                "Punto Fijo": 5.0   # Muy dependiente del despeje
            }
            score_robust_izq = robustness_scores.get(nom_1, 5.0)
            score_robust_der = robustness_scores.get(nom_2, 5.0)

            # Armamos las listas de puntajes para cada método [Vel, Costo, Robust]
            scores_izq = [score_vel_izq, score_costo_izq, score_robust_izq]
            scores_der = [score_vel_der, score_costo_der, score_robust_der]

            # --- B. Renderizado del Gráfico de Radar ---
            with col_ver2:
                # ¡Aquí está la gráfica de celulares que querías!
                grafico.dibujar_radar_veredicto(nom_1, scores_izq, nom_2, scores_der)

            # --- C. Veredicto de Texto (Opcional, en la columna izquierda) ---
            with col_ver1:
                st.markdown("##### Interpretación")
                st.write("""
                Este gráfico de radar muestra el equilibrio de poder de los métodos en una escala del 0 al 10.
                - **Mayor área:** Método más 'equilibrado' para esta función específica.
                - **Newton** suele ganar en *Velocidad* pero perder en *Robustez*.
                - **Bisección** siempre ganará en *Robustez* pero perderá en *Velocidad*.
                """)