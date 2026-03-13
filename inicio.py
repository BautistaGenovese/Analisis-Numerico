import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json

def cargar_lottie_local(ruta_archivo: str):
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return json.load(f)
def inicio():

    # 1. CSS para sacar los márgenes blancos y que la imagen toque los bordes
    #st.markdown("""
    #    <style>
    #    /* Esto elimina el espacio en blanco de arriba y los costados */
    #    .block-container {
    #        padding-top: 0rem !important;
    #        padding-bottom: 0rem !important;
    #    }
    #    </style>
    #""", unsafe_allow_html=True)

    # 2. Cargamos la imagen de portada
    # Asegurate de poner la ruta correcta donde guardaste tu imagen
    #st.image("fondoCalculadoras.jpg", use_container_width=True)"""

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

    # --- CSS ACTUALIZADO PARA 5 COLUMNAS ---
    st.markdown("""
        <style>
        /* Diseño base de los botones */
        .stButton > button {
            height: 110px;
            border-radius: 10px;
            border: none;
            transition: 0.3s;
        }
        
        /* Letra de los botones (un poco más chica para que entren 3 por fila) */
        .stButton > button p {
            font-size: 24px !important; 
            font-family: 'Verdana', sans-serif !important; 
            font-weight: bold !important;
            color: white !important;
        }

        /* 1er botón (Bisección) - Rojo */
        div[data-testid="stColumn"]:nth-of-type(1) .stButton > button { background-color: #FF4B4B !important; }
        div[data-testid="stColumn"]:nth-of-type(1) .stButton > button:hover { background-color: #ff7676 !important; }

        /* 2do botón (Regula Falsi) - Verde */
        div[data-testid="stColumn"]:nth-of-type(2) .stButton > button { background-color: #00CC96 !important; }
        div[data-testid="stColumn"]:nth-of-type(2) .stButton > button:hover { background-color: #33d6a8 !important; }

        /* 3er botón (Newton) - Azul */
        div[data-testid="stColumn"]:nth-of-type(3) .stButton > button { background-color: #0078D7 !important; }
        div[data-testid="stColumn"]:nth-of-type(3) .stButton > button:hover { background-color: #3b9cfa !important; }

        /* 4to botón (Secante) - Naranja */
        div[data-testid="stColumn"]:nth-of-type(4) .stButton > button { background-color: #FFA500 !important; }
        div[data-testid="stColumn"]:nth-of-type(4) .stButton > button:hover { background-color: #ffc04d !important; }

        /* 5to botón (Tangente) - Violeta */
        div[data-testid="stColumn"]:nth-of-type(5) .stButton > button { background-color: #8A2BE2 !important; }
        div[data-testid="stColumn"]:nth-of-type(5) .stButton > button:hover { background-color: #a454f0 !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- FUNCIONES DE NAVEGACIÓN ---
    def ir_a_biseccion():
        st.session_state.pagina_actual = "Bisección" 

    def ir_a_secante():
        st.session_state.pagina_actual = "Secante" 
    
    def ir_a_newton():
        st.session_state.pagina_actual = "Newton"

    def ir_a_puntofijo():
        pass

    def ir_a_tangente():
        pass

    # --- SECCIÓN 1: MÉTODOS CERRADOS ---
    st.markdown("### Métodos Cerrados")
    col1, col2 = st.columns(2)

    with col1:
        st.button("Bisección", use_container_width=True, on_click=ir_a_biseccion)
    with col2:
        st.button("Secante", use_container_width=True, on_click=ir_a_secante) 

    st.write("") # Un espacio en blanco para separar un poco

    # --- SECCIÓN 2: MÉTODOS ABIERTOS ---
    st.markdown("### Métodos Abiertos")
    col3, col4, col5 = st.columns(3)

    with col3:
        st.button("Newton", use_container_width=True, on_click=ir_a_newton)
    with col4:
        st.button("Punto Fijo", use_container_width=True, on_click=ir_a_puntofijo)
    with col5:
        st.button("Tangente", use_container_width=True, on_click=ir_a_tangente)

    
        

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
