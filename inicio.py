import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json

def cargar_lottie_local(ruta_archivo: str):
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return json.load(f)
def inicio():
    lottie_welcome = cargar_lottie_local("animaciones/Welcome.json")
    st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
    if lottie_welcome:
        
        st_lottie(
            lottie_welcome,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=200, 
            width=None, 
            key="large_welcome_animation",
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Métodos de búsqueda de raíces")

    st.markdown("""
        <style>
        /* Apuntamos a la clase genérica de botones de Streamlit */
        .stButton > button {
            height: 100px;
            border-radius: 10px;
            border: none;
            transition: 0.3s;
        }
                
        .stButton > button p {
            font-size: 28px !important; 
            font-family: 'Stoked', sans-serif !important; 
            font-weight: bold !important;
            color: white !important;
        }
                
        /* --- COLUMNA 1 (Izquierda) --- */
        /* 1er botón (Bisección) - Rojo */
        div[data-testid="stColumn"]:nth-of-type(1) div.element-container:nth-of-type(1) .stButton > button { background-color: #FF4B4B !important; }
        div[data-testid="stColumn"]:nth-of-type(1) div.element-container:nth-of-type(1) .stButton > button:hover { background-color: #ff7676 !important; }

        /* 2do botón (Newton) - Azul */
        div[data-testid="stColumn"]:nth-of-type(1) div.element-container:nth-of-type(2) .stButton > button { background-color: #0078D7 !important; }
        div[data-testid="stColumn"]:nth-of-type(1) div.element-container:nth-of-type(2) .stButton > button:hover { background-color: #3b9cfa !important; }

        /* 3er botón (Regula Falsi) - Violeta */
        div[data-testid="stColumn"]:nth-of-type(1) div.element-container:nth-of-type(3) .stButton > button { background-color: #9325c2 !important; }
        div[data-testid="stColumn"]:nth-of-type(1) div.element-container:nth-of-type(3) .stButton > button:hover { background-color: #b44ce0 !important; }
        
        /* --- COLUMNA 2 (Derecha) --- */
        /* 1er botón (Secante) - Verde */
        div[data-testid="stColumn"]:nth-of-type(2) div.element-container:nth-of-type(1) .stButton > button { background-color: #10c45b !important; }
        div[data-testid="stColumn"]:nth-of-type(2) div.element-container:nth-of-type(1) .stButton > button:hover { background-color: #6ae68f !important; }

        /* 2do botón (Tangente) - Naranja */
        div[data-testid="stColumn"]:nth-of-type(2) div.element-container:nth-of-type(2) .stButton > button { background-color: #FFA500 !important; }
        div[data-testid="stColumn"]:nth-of-type(2) div.element-container:nth-of-type(2) .stButton > button:hover { background-color: #ffc04d !important; }        
        
        </style>
    """, unsafe_allow_html=True)

    # --- FUNCIONES DE NAVEGACIÓN ---
    def ir_a_biseccion():
        st.session_state.pagina_actual = "Bisección" 

    def ir_a_secante():
        st.session_state.pagina_actual = "Secante" 
    
    def ir_a_newton():
        st.session_state.pagina_actual = "Newton"

    def ir_a_regulafalsi():
        pass

    def ir_a_tangente():
        pass

    # --- 3. BOTONES ---
    col1, col2 = st.columns(2)

    with col1:
        btn_biseccion = st.button("Bisección", use_container_width=True, on_click=ir_a_biseccion)
        btn_newton = st.button("Newton", use_container_width=True, on_click = ir_a_newton)
        btn_regulafalsi = st.button("Regula Falsi", use_container_width=True, on_click = ir_a_regulafalsi)
    with col2:
        btn_secante = st.button("Secante", use_container_width=True, on_click=ir_a_secante)
        btn_tangente = st.button("Tangente", use_container_width=True, on_click = ir_a_tangente)
    
        



    #st.header('Introducción')
    st.write("""
    - **Materia:** Análisis Numérico
    - **Docente:** Mauricio Orellana
    - **Objetivo general:** Desarrollar, implementar y analizar métodos numéricos aplicados a problemas reales.
    """)
    
    st.divider()

    st.header("👥 Integrantes del Equipo")

    data = {
        "Integrante": ["Bauti", "Mica", "Juan", "Net", "Trini", "Brisa", "Manu"],
        "Rol": ["Desarrollo", "Coordinación", "Documentación", "Testing", "Diseño", "Revisión", "Comunicación"],
    }

    df_integrantes = pd.DataFrame(data)
    st.dataframe(df_integrantes,hide_index=True)

    st.divider()

    st.header("🎯 Objetivos del Grupo")

    st.write("""
    - Comprender y aplicar métodos numéricos fundamentales.  
    - Desarrollar implementaciones en Python/Streamlit.  
    - Documentar resultados y análisis.  
    - Fomentar el trabajo colaborativo y la revisión cruzada.
    """)

    st.divider()

    st.header("🛠️ Herramientas Utilizadas")

    st.write("""
    - **Lenguajes:** Python  
    - **Librerías:** NumPy, SciPy, Matplotlib, Pandas  
    - **Plataformas:** GitHub, Streamlit  
    - **Metodologías:** Control de versiones, issues, branches
    """)

    st.divider()

    st.header("📚 Contenidos Abordados")

    st.write("""
    - Error numérico y estabilidad  
    - Métodos para ecuaciones no lineales  
    - Interpolación y aproximación
    """)

    st.divider()

    st.header("🧪 Actividades y Proyectos Realizados")

    st.write("""
    - Implementación de métodos numéricos en Python  
    - Desarrollo de una app interactiva en Streamlit  
    - Análisis de resultados y comparación de métodos  
    - Documentación en GitHub
    """)

    st.divider()

    st.header("📈 Resultados y Conclusiones")

    st.write("""
    - Se lograron implementar correctamente los métodos estudiados.  
    - Se identificaron desafíos en estabilidad y convergencia.  
    - El trabajo colaborativo permitió mejorar la calidad del código.  
    - Se proponen mejoras para futuras versiones de la app.
    """)
