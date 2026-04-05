import streamlit as st
import time

from metodos.metodo_numerico import MetodoNumerico
from metodos.biseccion import Biseccion
from metodos.regula_falsi import Regula_Falsi
from metodos.newton import Newton
from metodos.punto_fijo import PuntoFijo
from metodos.secante import Secante

from core import grafico

# Instanciamos cada método una sola vez
# Para agregar uno nuevo: solo agregarlo acá
METODOS = [
    Biseccion(),
    Regula_Falsi(),
    Newton(),
    PuntoFijo(),
    Secante()
]

# Construimos el diccionario dinámicamente desde las propiedades de cada clase
# La key es "Bisección", "Newton", etc.
METODOS_DICT = {f"{m.nombre}": m for m in METODOS}

class Comparacion(MetodoNumerico):
    
    @property
    def nombre(self): return "Comparación de Métodos"
    
    def ejecutar(self, f, err, **params):
        return super().ejecutar(f, err, **params)
    
    def render_teoria(self):
        with st.expander("🥊 ¿Cómo funciona la Arena de Batalla?"):
            st.markdown("""
            **Concepto básico:** Esta sección enfrenta a dos algoritmos cara a cara bajo las **mismas condiciones exactas** (misma función $f(x)$ y misma tolerancia). El objetivo no es solo ver quién encuentra la raíz, sino evaluar **qué tan eficientes son** en el proceso.
            
            **Métricas de Evaluación:**
            * ⏱️ **Iteraciones y Tiempo (ms):** Mide la velocidad bruta. Ojo: un método con menos iteraciones no siempre es el más rápido en milisegundos si sus cálculos internos son muy pesados (ej. calcular derivadas complejas).
            * 🧮 **Cálculos de $f(x)$ (Costo Computacional):** Es la "moneda" del análisis numérico. Métodos como Newton evalúan la función y su derivada en cada paso (costo = 2 por iteración), mientras que la Secante o Regula Falsi reciclan valores anteriores (costo ≈ 1 por iteración después del arranque).
            * 🛡️ **Robustez:** Es el puntaje teórico de confiabilidad. La Bisección tiene puntaje perfecto porque jamás falla si hay cambio de signo, mientras que los métodos abiertos tienen menor puntaje por su riesgo de divergencia.
            """)
            
            st.info("""
            📊 **El Veredicto (Gráfico de Radar):** Al final de la batalla, Roooty normaliza estas métricas en una escala del 0 al 10 para trazar un gráfico de radar. 
            * **Velocidad:** Premia al que tardó menos tiempo.
            * **Costo:** Premia al que evaluó la función menos veces.
            * **Robustez:** Evalúa la estabilidad teórica del método.
            
            💡 **Tip:** El método ganador suele ser el que dibuja el **área más grande y equilibrada** en el radar. ¡Un Ferrari (Newton) no sirve si se estrella en la primera curva por una división por cero!
            """)

    def render_inputs(self):
        return super().render_inputs()
    
    def mostrar_codigo(self):
        return super().mostrar_codigo()
    
    def get_rango_grafico(self, raiz, **params):
        return super().get_rango_grafico(raiz, **params)

    def mostrar_info(self):
        st.title(self.nombre)
        # st.markdown(f"<h1 style='text-align: center;'>{self.nombre}</h1>", unsafe_allow_html=True)
        
        self.render_teoria()
        
        with st.container(border=True):
            st.subheader("📥 Ingreso de datos")
            
            # Datos Globales
            f, err, exponente_err = self.render_formula()

            # Selectores "VS"
            col1, col2, col3 = st.columns([2, 1, 2], gap="small")
            with col1:
                opc1 = st.selectbox('Rincón Azul:', key='opc1', index=None, options=list(METODOS_DICT.keys()))
            with col2:
                st.markdown("<h2 style='text-align: center; font-weight:800; margin-top: 15px;'>VS</h2>", unsafe_allow_html=True)
            with col3:
                opc2 = st.selectbox('Rincón Rojo:', key='opc2', index=None, options=list(METODOS_DICT.keys()))

            if opc1 is None or opc2 is None:
                st.info('🧮 Selecciona dos métodos en los menús de arriba para comenzar la batalla.')
            elif opc1 == opc2:
                st.warning('⚠️ Por favor, elige métodos distintos para poder compararlos.')
            else:
                st.divider()
                
                metodo1 = METODOS_DICT[opc1]
                metodo2 = METODOS_DICT[opc2]
                
                met1, met2 = st.columns(2, gap="large")
                with met1:
                    params1 = metodo1.render_inputs(key=f'inp_{opc1}')
                    inicio1 = time.perf_counter()
                    raiz_1, datos_1 = metodo1.ejecutar(f,err,**params1)
                    fin1 = time.perf_counter()
                    tiempo_1 = (fin1 - inicio1) * 1000
                    
                with met2:
                    params2 = metodo2.render_inputs(key=f'inp_{opc2}')
                    inicio2 = time.perf_counter()
                    raiz_2, datos_2 = metodo2.ejecutar(f,err,**params2)
                    fin2 = time.perf_counter()
                    tiempo_2 = (fin2 - inicio2) * 1000
                
                # === MÉTRICAS RÁPIDAS Y GRÁFICO FINAL ===
                if raiz_1 is not None and raiz_2 is not None:
                    # Obtengo los límites del grafico 
                    inf1, sup1 = metodo1.get_rango_grafico(raiz_1,**params1)
                    inf2, sup2 = metodo2.get_rango_grafico(raiz_2,**params2)
                    
                    # Genero los graficos
                    graf_1 = grafico.obtener_grafico(f, raiz_1, inf1, sup1, key=f'graf_{opc1.lower()}', iteraciones=datos_1.obtener_datos())
                    graf_2 = grafico.obtener_grafico(f, raiz_2, inf2, sup2, key=f'graf_{opc2.lower()}', iteraciones=datos_2.obtener_datos())
                    
                    # Grafico
                    col_g1, col_g2 = st.columns(2)
                    with col_g1:
                        st.success(f'Raíz encontrada en: $x \\approx {raiz_1:.6f}$')
                        with st.spinner(text='Generando grafica...'):
                            grafico.dibujar(graf_1,key=f'graf_{opc1.lower()}')
                    with col_g2:
                        st.success(f'Raíz encontrada en: $x \\approx {raiz_2:.6f}$')
                        with st.spinner(text='Generando grafica...'):
                            grafico.dibujar(graf_2,key=f'graf_{opc2.lower()}')
                    
                    with st.expander("📊 Ver tablas detalladas de iteraciones"):
                        col_t1, col_t2 = st.columns(2)
                        with col_t1:
                            st.markdown(f"**{opc1}**")
                            st.dataframe(datos_1.obtener_dataframe(),width='stretch')
                        with col_t2:
                            st.markdown(f"**{opc2}**")
                            st.dataframe(datos_2.obtener_dataframe(),width='stretch')
                               
                    st.divider()
                    st.subheader("🏆 Resultados de la Comparación")
                    
                    # Recuperamos datos crudos
                    d_izq = datos_1.obtener_datos()
                    d_der = datos_2.obtener_datos()
                    iters_1 = len(d_izq['x[i]'])
                    iters_2 = len(d_der['x[i]'])

                    costo_1 = 2 + iters_1 if opc1 != "Newton" else 2 * iters_1
                    costo_2 = 2 + iters_2 if opc2 != "Newton" else 2 * iters_2
                    
                    # --- DISEÑO DE BATALLA (Limpio y Nativo) ---
                    st.markdown("<br>", unsafe_allow_html=True) # Un espaciecito extra para que respire
                    
                    # Usamos 2 columnas simples, sin márgenes raros
                    col_azul, col_rojo = st.columns(2, gap="large")

                    with col_azul:
                        st.markdown(f"<h3 style='color: #3498DB;'>🔵 {opc1}</h3>", unsafe_allow_html=True)
                        
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
                        st.markdown(f"<h3 style='color: #E74C3C;'>🔴 {opc2}</h3>", unsafe_allow_html=True)
                        
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
                        opc1, 
                        opc2
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
                        "Bisección": 10.0, # Garantizado si hay cambio de signo
                        "Regula Falsi": 6.5,   # Prima hermana de la secante, misma robustez
                        "Secante": 6.5,    # Abierto, pero más estable
                        "Newton": 4.0,     # Rápido pero diverge fácil por f'(x) = 0
                        "Punto Fijo": 5.0  # Muy dependiente del despeje
                    }
                    
                    score_robust_izq = robustness_scores.get(opc1, 5.0)
                    score_robust_der = robustness_scores.get(opc2, 5.0)

                    # Armamos las listas de puntajes para cada método [Vel, Costo, Robust]
                    scores_izq = [score_vel_izq, score_costo_izq, score_robust_izq]
                    scores_der = [score_vel_der, score_costo_der, score_robust_der]

                    # --- B. Renderizado del Gráfico de Radar ---
                    with col_ver2:
                        # ¡Aquí está la gráfica de celulares que querías!
                        grafico.dibujar_radar_veredicto(opc1, scores_izq, opc2, scores_der)

                    # --- C. Veredicto de Texto (Opcional, en la columna izquierda) ---
                    with col_ver1:
                        st.markdown("##### Interpretación")
                        st.write("""
                        Este gráfico de radar muestra el equilibrio de poder de los métodos en una escala del 0 al 10.
                        - **Mayor área:** Método más 'equilibrado' para esta función específica.
                        - **Newton** suele ganar en *Velocidad* pero perder en *Robustez*.
                        - **Bisección** siempre ganará en *Robustez* pero perderá en *Velocidad*.
                        """)

                else:
                    st.error('😥 No se ha encontrado la raíz o uno de los métodos diverge.')

if __name__ == "__main__":
    app = Comparacion()
    app.mostrar_info()