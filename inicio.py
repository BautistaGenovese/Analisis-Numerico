import streamlit as st
import json

# Intenta importar streamlit_lottie, si no está, no rompe la app
try:
    from streamlit_lottie import st_lottie
    LOTTIE_DISPONIBLE = True
except ImportError:
    LOTTIE_DISPONIBLE = False

def cargar_lottie_local(ruta_archivo: str):
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return json.load(f)

def inicio():
    # --- CSS MÁGICO PARA LAS TARJETAS CON HOVER ---
    estilos_css = """
    <style>
    .feature-card {
        background-color: rgba(40, 44, 52, 0.4);
        border: 2px solid #3d434f;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease-in-out;
        height: 100%;
        color: #e0e0e0;
        user-select: none; 
    }
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 25px rgba(52, 152, 219, 0.4);
        border-color: #3498DB;
    }
    .feature-card h4 {
        color: #3498DB;
        margin-top: 0;
        font-weight: 700;
    }
    .competencia-box {
        background-color: rgba(231, 76, 60, 0.1);
        border-left: 4px solid #E74C3C;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin-top: 20px;
    }
    </style>
    """
    st.markdown(estilos_css, unsafe_allow_html=True)
    st.write("")
    
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

    # Centramos el texto con etiquetas HTML
    st.markdown("<h1 style='text-align: center; font-size: 4.5rem; margin-bottom: 0; line-height: 1.1;'><i>Roooty </i><span style='color: #3498DB;'>🚀</span></h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #bdc3c7; margin-top: 10px;'>Tu laboratorio interactivo de Análisis Numérico</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #a0aab5; max-width: 800px; margin: 0 auto;'>Olvidate de hacer iteraciones a mano en papel. Roooty automatiza, grafica y compara los algoritmos matemáticos más potentes para encontrar raíces de funciones no lineales en milisegundos.</p>", unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.divider()

    # --- 2. SUPERPODERES (Con CSS Hover) ---
    st.markdown("### ✨ ¿Qué hace especial a Roooty?")
    st.write("")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Precisión Dinámica</h4>
            <p>Controlá la tolerancia al milímetro. Simulá aritmética finita y configurá el <i>cero máquina</i> a tu gusto para ver cómo explotan (o sobreviven) los métodos.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="feature-card">
            <h4>🥊 Arena de Batalla</h4>
            <p>Enfrentá a Newton contra la Secante en la sección de <b>Comparación</b>. Medí el tiempo de ejecución, cantidad de iteraciones y descubrí quién es el rey.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="feature-card">
            <h4>📄 Reportes Premium</h4>
            <p>Con un solo clic, exportá un PDF profesional con la gráfica, la tabla de iteraciones detallada y todos los parámetros de tu cálculo. Ideal para el TP.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.divider()

    # --- 3. EL ARSENAL NUMÉRICO Y LA COMPETENCIA ---
    st.markdown("### 🧮 Nuestro Arsenal Numérico")
    st.write("Explorá los algoritmos disponibles en el menú de navegación izquierdo:")
    
    tab1, tab2, tab3 = st.tabs(["🔒 Métodos Cerrados", "⚡ Métodos Abiertos", "📈 Regresión"])
    
    with tab1:
        st.success("**Bisección:** El viejo y confiable. Encierra la raíz en un intervalo y lo parte a la mitad. Lento pero 100% seguro (siempre que haya cambio de signo).")
    with tab2:
        st.info("**Newton-Raphson:** Usa derivadas para trazar tangentes. Un Fórmula 1 matemático.\n\n**Secante / Tangente:** Aproxima la derivada usando puntos anteriores.\n\n**Punto Fijo:** Transforma la función y busca el punto de cruce con la identidad.")
    with tab3:
        st.warning("**Regresión Lineal:** Ajusta la mejor recta posible a una nube de puntos experimentales utilizando el método de mínimos cuadrados.")

    # Tiradera a la competencia
    st.markdown("""
    <div class="competencia-box">
        <h4 style="margin-top: 0; color: #E74C3C;">🔥 ¿Por qué aplastamos a la competencia?</h4>
        <ul style="margin-bottom: 0;">
            <li><b>vs. WolframAlpha / Symbolab:</b> Ellos te cobran la suscripción PRO para ver el "paso a paso". Roooty te da la tabla de iteraciones completa y el error de propagación <b>totalmente gratis</b>.</li>
            <li><b>vs. GeoGebra:</b> Grafica lindo, pero no te permite simular aritmética finita (truncamiento) ni enfrentar dos algoritmos cara a cara con métricas de rendimiento.</li>
            <li><b>vs. Excel:</b> Olvidate de arrastrar celdas y romper fórmulas. En Roooty ingresás la función, tocás un botón y tenés tu PDF listo para entregar.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    # --- 4. EL EQUIPO (Integrantes) ---
    st.markdown("### 👨‍💻 El Escuadrón detrás del Código")
    st.write("Este proyecto fue desarrollado con sangre, sudor, matemáticas y mucho café por estas 7 leyendas:")
    st.write("")
    
    # Primera fila: 4 integrantes
    f1_1, f1_2, f1_3, f1_4 = st.columns(4)
    
    with f1_1:
        st.markdown("#### 🧑‍🚀 Bautista Genovese")
        st.caption("Rol: Arquitecto de Software")
        st.write("Encargado de la refactorización extrema y de pelear mano a mano con la librería de Plotly.")
        
    with f1_2:
        st.markdown("#### 🕵️‍♂️ Ignacio Giangrieco")
        st.caption("Rol: Maestro de Algoritmos")
        st.write("Dominador absoluto de los bucles `while` y cazador implacable de divisiones por cero.")
        
    with f1_3:
        st.markdown("#### 🧞‍♂️ Juan Giron")
        st.caption("Rol: Recolector de ideas")
        st.write("Es el puente que organiza y traduce esas chispas sueltas en la base sólida de un nuevo proyecto.")
        
    with f1_4:
        st.markdown("#### 🎨 Trini Kildegaard")
        st.caption("Rol: UX/UI & CSS Ninja")
        st.write("El artista. Si la app se ve fachera y no te quema los ojos, es gracias a su magia.")

    st.write("") # Espaciador entre filas
    
    # Segunda fila: 3 integrantes
    f2_1, f2_2, f2_3 = st.columns(3)
    
    with f2_1:
        st.markdown("#### 🧉 Brisa Romero")
        st.caption("Rol: Scrum Master & Mates")
        st.write("Líder espiritual. Mantuvo la moral alta y el termo siempre lleno en las madrugadas de código.")
        
    with f2_2:
        st.markdown("#### 🧙‍♂️ Micaías Villa")
        st.caption("Rol: Git Master & DevOps")
        st.write("El salvador de los *merge conflicts*. Su único miedo es que no compile en la PC del profe.")
        
    with f2_3:
        st.markdown("#### 🧠 Manuel Montoya")
        st.caption("Rol: Criptógrafo Matemático")
        st.write("Traductor oficial. El único capaz de descifrar qué pedía realmente la cátedra en el PDF.")

    st.write("")
    st.write("")
    
    # --- 5. ZONA DE ADVERTENCIA TÉCNICA ---
    st.warning(
        "**Tip de Supervivencia:** Recuerda que los métodos abiertos (como Newton o Punto Fijo) no garantizan la convergencia. "
        "Si la app te dice que el método divergió, no te asustes: intenta cambiar tu $x_0$ inicial o el límite de divergencia en la ⚙️ Configuración Global.",
        icon="💡"
    )

if __name__ == '__main__':
    inicio()
