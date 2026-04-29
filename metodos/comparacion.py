import streamlit as st
import time

from metodos.metodo_numerico import MetodoNumerico
from metodos.biseccion import Biseccion
from metodos.regula_falsi import Regula_Falsi
from metodos.newton import Newton
from metodos.punto_fijo import PuntoFijo
from metodos.secante import Secante
from core import grafico, utils as ut

METODOS = [Biseccion(), Regula_Falsi(), Newton(), PuntoFijo(), Secante()]
METODOS_DICT = {f"{m.nombre}": m for m in METODOS}

class Comparacion(MetodoNumerico):
    
    @property
    def nombre(self): return "Análisis Comparativo"
    
    @property
    def categoria(self): return "HERRAMIENTA DE DIAGNÓSTICO"    
    
    def ejecutar(self, f, err, **params): return super().ejecutar(f, err, **params)
    def render_teoria(self):
        with st.expander("📖 Sobre el Análisis Comparativo"):
            st.markdown("""
            **Objetivo:** Evaluar el rendimiento relativo de dos algoritmos bajo condiciones idénticas. 
            Este panel permite contrastar la velocidad de convergencia y el costo computacional de los métodos seleccionados.
            """)

    def render_inputs(self): return super().render_inputs()
    def mostrar_codigo(self): return super().mostrar_codigo()
    def get_rango_grafico(self, raiz, **params): return super().get_rango_grafico(raiz, **params)

    def mostrar_info(self):
        st.title(self.nombre)
        self.render_teoria()
        
        # 🔒 RECUPERAR MEMORIA
        llave_memoria = "memoria_comparacion"
        f_guardada = ""
        if llave_memoria in st.session_state and st.session_state[llave_memoria] is not None:
            f_guardada = st.session_state[llave_memoria]['f']

        with st.container(border=True):
            # st.markdown("#### 🛠️ Configuración del Análisis")
            st.markdown(f"""
                <div style='display:flex; align-items:center; flex-wrap: wrap; margin: 8px 0 15px 0;'>
                    <h4 style='margin:auto; padding: 6px 8px 8px 0'><b>Configuración del Análisis</b></h4>
                    <b style=' padding:0 4px; background-color: #cfe5fc; border-radius:3px; margin:auto 0; color:#3b82f6;'>EVALUACIÓN DE RENDIMIENTO</b>
                </div>
            """, unsafe_allow_html=True)
            
            # 1. Función y Tolerancia (Global)
            f, err, exp_err = self.render_formula(valor_default=f_guardada)

            st.divider()

            # 2. SELECCIÓN Y PARÁMETROS 
            col_met_a, col_met_b = st.columns(2, gap="large")
            
            with col_met_a:
                st.markdown("<p style='color: #3b82f6; font-weight: 800; margin-bottom: 0;'>MÉTODO A</p>", unsafe_allow_html=True)
                opc1 = st.selectbox('Seleccionar Algoritmo', key='opc1', index=None, options=list(METODOS_DICT.keys()), label_visibility="collapsed")
                
                params1 = {}
                if opc1:
                    with st.container():
                        params1 = METODOS_DICT[opc1].render_inputs(key=f'inp_{opc1}')
            
            with col_met_b:
                st.markdown("<p style='color: #8b5cf6; font-weight: 800; margin-bottom: 0;'>MÉTODO B</p>", unsafe_allow_html=True)
                opc2 = st.selectbox('Seleccionar Algoritmo', key='opc2', index=None, options=list(METODOS_DICT.keys()), label_visibility="collapsed")
                
                params2 = {}
                if opc2:
                    with st.container():
                        params2 = METODOS_DICT[opc2].render_inputs(key=f'inp_{opc2}')

            st.markdown("<br>", unsafe_allow_html=True)
            calcular_btn = st.button("🚀 Ejecutar Análisis Comparativo", type="primary", use_container_width=True)

            if calcular_btn:
                if f.strip() == "" or opc1 is None or opc2 is None:
                    st.warning("⚠️ Asegúrate de ingresar una función y seleccionar ambos métodos.")
                elif opc1 == opc2:
                    st.warning('⚠️ Elige métodos distintos para comparar.')
                else:
                    # Ejecución
                    met1, met2 = METODOS_DICT[opc1], METODOS_DICT[opc2]
                    
                    i1 = time.perf_counter()
                    raiz_1, datos_1 = met1.ejecutar(f, err, **params1)
                    t1 = (time.perf_counter() - i1) * 1000
                    
                    i2 = time.perf_counter()
                    raiz_2, datos_2 = met2.ejecutar(f, err, **params2)
                    t2 = (time.perf_counter() - i2) * 1000
                    
                    st.session_state[llave_memoria] = {
                        'f': f, 'opc1': opc1, 'opc2': opc2,
                        'r1': raiz_1, 'd1': datos_1, 't1': t1, 'p1': params1,
                        'r2': raiz_2, 'd2': datos_2, 't2': t2, 'p2': params2
                    }

        # --- PANEL DE RESULTADOS ---
        if llave_memoria in st.session_state and st.session_state[llave_memoria] is not None:
            mem = st.session_state[llave_memoria]
            
            if mem['r1'] is not None and mem['r2'] is not None:
                st.divider()
                
                # TÍTULO SUTIL
                st.markdown("""
                    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px; margin-top: 10px;">
                        <div style="background-color: #f8fafc; padding: 6px 18px; border-radius: 30px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                            <span style="color: #475569; font-weight: 800; font-size: 0.75rem; letter-spacing: 1.5px;">🔬 FUNCIÓN EN ANÁLISIS</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # 🚀 FÓRMULA EN TAMAÑO "HUGE"
                # Usamos \Huge dentro del string de LaTeX para forzar el tamaño máximo de KaTeX
                formula_latex = ut.mostrar_formula(self.get_formula_grafico(mem['f']))
                st.latex(f"\\large {formula_latex}")
                
                # Espacio extra para que los gráficos no queden pegados a la fórmula gigante
                st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

                # SECCIÓN DE GRÁFICOS (Continúa el resto de tu código...)
                col_g1, col_g2 = st.columns(2)
                
                m1, m2 = METODOS_DICT[mem['opc1']], METODOS_DICT[mem['opc2']]
                inf1, sup1 = m1.get_rango_grafico(mem['r1'], **mem['p1'])
                inf2, sup2 = m2.get_rango_grafico(mem['r2'], **mem['p2'])
                
                with col_g1:
                    with st.container(border=True): # ✅ Fondo blanco
                        st.markdown(f"<p style='text-align: center; color: #3b82f6; font-weight: 700; margin-bottom: 0;'>{mem['opc1'].upper()}</p>", unsafe_allow_html=True)
                        g1 = grafico.obtener_grafico(mem['f'], mem['r1'], inf1, sup1, key=f"g_{mem['opc1']}", iteraciones=mem['d1'].obtener_datos())
                        grafico.dibujar(g1, key=f"dg_{mem['opc1']}")
                
                with col_g2:
                    with st.container(border=True): # ✅ Fondo blanco
                        st.markdown(f"<p style='text-align: center; color: #8b5cf6; font-weight: 700; margin-bottom: 0;'>{mem['opc2'].upper()}</p>", unsafe_allow_html=True)
                        g2 = grafico.obtener_grafico(mem['f'], mem['r2'], inf2, sup2, key=f"g_{mem['opc2']}", iteraciones=mem['d2'].obtener_datos())
                        grafico.dibujar(g2, key=f"dg_{mem['opc2']}")

                # MÉTRICAS DE RENDIMIENTO HTML
                d_izq, d_der = mem['d1'].obtener_datos(), mem['d2'].obtener_datos()
                it1, it2 = len(d_izq['x[i]']), len(d_der['x[i]'])
                c1 = 2 + it1 if mem['opc1'] != "Newton" else 2 * it1
                c2 = 2 + it2 if mem['opc2'] != "Newton" else 2 * it2

                html_kpi = f"""
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                    <div style="display: flex; background: #f8fafc; border-bottom: 1px solid #e2e8f0; padding: 12px;">
                        <div style="flex: 1; text-align: center; font-weight: 800; color: #3b82f6;">{mem['opc1']}</div>
                        <div style="flex: 0.8; text-align: center; font-weight: 600; color: #64748b; font-size: 0.8rem; align-self: center;">MÉTRICAS</div>
                        <div style="flex: 1; text-align: center; font-weight: 800; color: #8b5cf6;">{mem['opc2']}</div>
                    </div>
                    <div style="display: flex; border-bottom: 1px solid #f1f5f9; padding: 15px;">
                        <div style="flex: 1; text-align: center; font-weight: 700; font-size: 1.2rem;">{mem['r1']:.6f}</div>
                        <div style="flex: 0.8; text-align: center; color: #94a3b8; font-size: 0.8rem; align-self: center;">Raíz Encontrada</div>
                        <div style="flex: 1; text-align: center; font-weight: 700; font-size: 1.2rem;">{mem['r2']:.6f}</div>
                    </div>
                    <div style="display: flex; border-bottom: 1px solid #f1f5f9; padding: 15px; background: #fafafa;">
                        <div style="flex: 1; text-align: center; font-weight: 700; font-size: 1.2rem;">{it1}</div>
                        <div style="flex: 0.8; text-align: center; color: #94a3b8; font-size: 0.8rem; align-self: center;">Iteraciones</div>
                        <div style="flex: 1; text-align: center; font-weight: 700; font-size: 1.2rem;">{it2}</div>
                    </div>
                    <div style="display: flex; padding: 15px; border-bottom: 1px solid #f1f5f9;">
                        <div style="flex: 1; text-align: center; font-weight: 700; font-size: 1.2rem;">{mem['t1']:.3f} ms</div>
                        <div style="flex: 0.8; text-align: center; color: #94a3b8; font-size: 0.8rem; align-self: center;">Tiempo Ejecución</div>
                        <div style="flex: 1; text-align: center; font-weight: 700; font-size: 1.2rem;">{mem['t2']:.3f} ms</div>
                    </div>
                    <div style="display: flex; padding: 15px; background: #fafafa;">
                        <div style="flex: 1; text-align: center; font-weight: 700; font-size: 1.2rem;">{c1}</div>
                        <div style="flex: 0.8; text-align: center; color: #94a3b8; font-size: 0.8rem; align-self: center;">Cálculos de f(x)</div>
                        <div style="flex: 1; text-align: center; font-weight: 700; font-size: 1.2rem;">{c2}</div>
                    </div>
                </div>
                """
                st.markdown(html_kpi, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # GRÁFICO DE ERRORES (En contenedor)
                with st.container(border=True): # Fondo blanco
                    grafico.dibujar_analisis_errores(d_izq, d_der, mem['opc1'], mem['opc2'])
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # RADAR E INFO (En contenedor)
                col_radar_info, col_radar_plot = st.columns([1, 2], gap="large")
                
                with col_radar_info:
                    # Regresó la interpretación perdida
                    st.markdown("##### 🎯 Interpretación del Radar")
                    st.info("""
                    Este gráfico normaliza las métricas en una escala de eficiencia del 0 al 10.
                    
                    - **Mayor área sombreada:** Indica un método globalmente más eficiente.
                    - **Newton** suele dominar en la *Velocidad* pero flaquea en *Robustez* por requerir derivadas que no se anulen.
                    - **Bisección** prioriza siempre la *Robustez* (siempre converge) a costa de una menor *Velocidad*.
                    """)

                with col_radar_plot:
                    with st.container(border=True): # Fondo blanco
                        # Lógica de puntajes
                        min_t = min(mem['t1'], mem['t2'])
                        s_vel1, s_vel2 = (min_t/mem['t1'])*10, (min_t/mem['t2'])*10
                        
                        min_c = min(c1, c2)
                        s_c1, s_c2 = (min_c/c1)*10, (min_c/c2)*10
                        
                        rob = {"Bisección": 10, "Regula Falsi": 6.5, "Secante": 6.5, "Newton": 4, "Punto Fijo": 5}
                        
                        grafico.dibujar_radar_analisis(
                            mem['opc1'], [s_vel1, s_c1, rob.get(mem['opc1'], 5)], 
                            mem['opc2'], [s_vel2, s_c2, rob.get(mem['opc2'], 5)]
                        )

            else:
                st.error('Divergencia detectada en uno de los métodos. No es posible generar el análisis.')

if __name__ == "__main__":
    app = Comparacion()
    app.mostrar_info()
