import streamlit as st

def inicio():
    st.markdown("""
<div class="hero-banner" style="background-color: #1a2b4c; border-radius: 15px; padding: 3rem; margin-bottom: 3rem; box-shadow: 0 10px 25px rgba(26,43,76,0.2);">
    <div class="hero-inner" style="display:flex; flex-direction:row; justify-content:space-between; align-items:center; gap:2rem; flex-wrap:wrap;">
        <div class="hero-text" style="flex:1; min-width:250px;">
            <span style="background-color:rgba(255,255,255,0.1); color:#ffffff; padding:5px 15px; border-radius:20px; font-size:0.8rem; font-weight:600; display:inline-block; margin-bottom:15px;">VERSIÓN BETA 🚀</span>
            <h1 style="color:#ffffff; font-size:3.5rem; margin:0 0 10px 0; font-weight:800; line-height:1.1; letter-spacing:-1px;">
                <b style="display:inline; padding:0px 21px; margin-right:5px; background-color:#ffffff; border-radius:5px; color:#1a2b4c;">Σ</b> ROOOTY
            </h1>
            <p style="color:#cbd5e1; font-size:1.1rem; line-height:1.5; margin:0;">Tu plataforma corporativa de Análisis Numérico diseñada para la precisión y el aprendizaje paso a paso.</p>
        </div>
        <div class="hero-anim" style="flex:1; min-width:250px; padding:1.5rem; background-color:rgba(255,255,255,0.03); border-radius:12px; position:relative; animation:flotar 4s ease-in-out infinite;">
            <div style="position:relative; width:100%; height:180px;">
                <div style="position:absolute; width:100%; height:1px; bottom:0; background-color:rgba(255,255,255,0.1);"></div>
                <div style="position:absolute; width:1px; height:100%; left:10%; background-color:rgba(255,255,255,0.1);"></div>
                <div style="position:absolute; bottom:20px; left:10%; width:80%; height:120px; border-bottom:3px solid transparent; border-left:3px solid transparent; border-radius:50% 50% 0 0; border-top:3px solid #00A38C;"></div>
                <div style="position:absolute; width:10px; height:10px; background-color:rgba(255,255,255,0.4); border-radius:50%; border:2px solid #FF6F91; bottom:80px; left:15%;"></div>
                <div style="position:absolute; width:10px; height:10px; background-color:rgba(255,255,255,0.4); border-radius:50%; border:2px solid #FF6F91; bottom:50px; left:25%;"></div>
                <div style="position:absolute; width:10px; height:10px; background-color:rgba(255,255,255,0.4); border-radius:50%; border:2px solid #FF6F91; bottom:60px; left:65%;"></div>
                <div style="position:absolute; width:14px; height:14px; background-color:#00A38C; border-radius:50%; bottom:100px; left:50%; transform:translate(-50%, 50%); animation:pulso_raiz 2s infinite;"></div>
                <span style="position:absolute; font-size:0.75rem; color:#ffffff; bottom:120px; left:45%;">Raíz Calculada</span>
                <span style="position:absolute; font-size:0.7rem; color:#cbd5e1; bottom:95px; left:18%;">Iteraciones</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    # --- 2. POR QUÉ ELEGIR ROOOTY ---
    st.markdown("<h2 style='text-align: center; color: #1a2b4c; font-weight: 800;'>¿Por qué elegir Roooty?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Elevamos el estándar del análisis numérico académico frente a las herramientas tradicionales.</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.info("#### 📑 Paso a paso gratis\nEllos te cobran la suscripción PRO para ver el 'paso a paso'. Roooty te da la tabla de iteraciones completa y el error de forma **totalmente gratis**.")
    with c2: st.success("#### 🎯 Aritmética finita\nNo permitimos errores mágicos. Simula aritmética finita (truncamiento) y maneja el número de cifras significativas (K) a tu gusto.")
    with c3: st.warning("#### 📄 Reportes Académicos\nOlvidate de arrastrar celdas en Excel. Ingresa la función, toca un botón y tenés tu PDF profesional listo para entregar en el TP.")

    st.markdown("<br><hr style='border-top: 1px solid #e2e8f0;'><br>", unsafe_allow_html=True)

    # --- 3. TABLA COMPARATIVA ---
    st.markdown("<h3 style='color: #1a2b4c;'>Tabla Comparativa</h3>", unsafe_allow_html=True)
    html_tabla = """
        <div style="overflow-x: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 2rem;">
            <table style="width:100%; min-width: 600px; text-align: left; border-collapse: collapse; background: white; margin: auto;">
                <tr style="border-bottom: 2px solid #e2e8f0; color: #64748b; font-size: 0.8rem; background-color: #f8fafc;">
                    <th style="padding: 15px; white-space: nowrap;">CARACTERÍSTICA</th>
                    <th style="padding: 15px; white-space: nowrap;">WOLFRAMALPHA</th>
                    <th style="padding: 15px; white-space: nowrap;">EXCEL / GEOGEBRA</th>
                    <th style="padding: 15px; color: #1a2b4c; white-space: nowrap;">ROOOTY</th>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 15px; color: #1e293b;">Pasos de iteración</td>
                    <td style="padding: 15px; color: #ef4444;">Pago (Pro)</td>
                    <td style="padding: 15px; color: #64748b;">Limitado / Manual</td>
                    <td style="padding: 15px; font-weight: bold; color: #1a2b4c;">Gratis & Ilimitado</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 15px; color: #1e293b;">Aritmética Finita</td>
                    <td style="padding: 15px; color: #64748b;">Automático</td>
                    <td style="padding: 15px; color: #64748b;">Estándar Rígido</td>
                    <td style="padding: 15px; font-weight: bold; color: #1a2b4c;">Configurable (K bits)</td>
                </tr>
                <tr>
                    <td style="padding: 15px; color: #1e293b;">Exportación Directa</td>
                    <td style="padding: 15px; color: #64748b;">Solo imagen</td>
                    <td style="padding: 15px; color: #64748b;">Manual / Formatos fijos</td>
                    <td style="padding: 15px; font-weight: bold; color: #1a2b4c;">PDF Dinámico</td>
                </tr>
            </table>
        </div>
    """
    st.markdown(html_tabla, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- 4. ARSENAL NUMÉRICO ---
    st.markdown("<h2 style='text-align: center; color: #1a2b4c; font-weight: 800;'>🎛️ Nuestro Arsenal Numérico</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Explorá los algoritmos disponibles en el menú de navegación izquierdo.</p>", unsafe_allow_html=True)
    
    colA, colB = st.columns(2)
    with colA:
        st.markdown("<b style='color: #475569;'>🔒 MÉTODOS CERRADOS</b>", unsafe_allow_html=True)
        st.markdown("""<div class='metodo-card'><b style='color:#1a2b4c; font-size: 1.1rem;'>Bisección</b><br><span style='color:#64748b; font-size: 0.9rem;'>El viejo y confiable. Encierra la raíz en un intervalo y lo parte a la mitad.</span></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='metodo-card'><b style='color:#1a2b4c; font-size: 1.1rem;'>Regula Falsi</b><br><span style='color:#64748b; font-size: 0.9rem;'>Aproximación lineal más rápida que la bisección manteniendo convergencia.</span></div><br>""", unsafe_allow_html=True)
    with colB:
        st.markdown("<b style='color: #475569;'>⚡ MÉTODOS ABIERTOS</b>", unsafe_allow_html=True)
        st.markdown("""<div class='metodo-card'><b style='color:#1a2b4c; font-size: 1.1rem;'>Newton-Raphson</b><br><span style='color:#64748b; font-size: 0.9rem;'>Dominador absoluto de los bucles con convergencia cuadrática.</span></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='metodo-card'><b style='color:#1a2b4c; font-size: 1.1rem;'>Secante</b><br><span style='color:#64748b; font-size: 0.9rem;'>Variante de Newton sin necesidad de derivar analíticamente.</span></div>""", unsafe_allow_html=True)

    st.markdown("<br><hr style='border-top: 1px solid #e2e8f0;'><br>", unsafe_allow_html=True)

    # --- 5. EL ESCUADRÓN ---
    st.markdown("<h3 style='text-align: center; color: #1a2b4c;'>👥 El Escuadrón detrás del Código</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Este proyecto fue desarrollado con sangre, sudor, matemáticas y mucho café por estas leyendas:</p>", unsafe_allow_html=True)
    
    html_escuadron = """
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; text-align: center; margin-top: 30px;">
            <div class='integrante-escuadron'><div style="background:#1e293b; color:white; width:60px; height:60px; border-radius:50%; line-height:60px; margin:0 auto; font-weight:bold; font-size: 1.1rem;">BG</div><span style='color:#1e293b; font-size: 0.8rem;'><b>Bautista</b></span></div>
            <div class='integrante-escuadron'><div style="background:#e0f2fe; color:#0284c7; width:60px; height:60px; border-radius:50%; line-height:60px; margin:0 auto; font-weight:bold; font-size: 1.1rem;">IG</div><span style='color:#1e293b; font-size: 0.8rem;'><b>Ignacio</b></span></div>
            <div class='integrante-escuadron'><div style="background:#f3e8ff; color:#9333ea; width:60px; height:60px; border-radius:50%; line-height:60px; margin:0 auto; font-weight:bold; font-size: 1.1rem;">JG</div><span style='color:#1e293b; font-size: 0.8rem;'><b>Juan</b></span></div>
            <div class='integrante-escuadron'><div style="background:#ffedd5; color:#ea580c; width:60px; height:60px; border-radius:50%; line-height:60px; margin:0 auto; font-weight:bold; font-size: 1.1rem;">TK</div><span style='color:#1e293b; font-size: 0.8rem;'><b>Trini</b></span></div>
            <div class='integrante-escuadron'><div style="background:#dcfce7; color:#16a34a; width:60px; height:60px; border-radius:50%; line-height:60px; margin:0 auto; font-weight:bold; font-size: 1.1rem;">BR</div><span style='color:#1e293b; font-size: 0.8rem;'><b>Brisa</b></span></div>
            <div class='integrante-escuadron'><div style="background:#f1f5f9; color:#475569; width:60px; height:60px; border-radius:50%; line-height:60px; margin:0 auto; font-weight:bold; font-size: 1.1rem;">MV</div><span style='color:#1e293b; font-size: 0.8rem;'><b>Micaías</b></span></div>
            <div class='integrante-escuadron'><div style="background:#fef9c3; color:#ca8a04; width:60px; height:60px; border-radius:50%; line-height:60px; margin:0 auto; font-weight:bold; font-size: 1.1rem;">MM</div><span style='color:#1e293b; font-size: 0.8rem;'><b>Manuel</b></span></div>
        </div>
    """
    st.markdown(html_escuadron, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.error("💡 **TIP DE SUPERVIVENCIA**\nRecuerda que los métodos abiertos no garantizan la convergencia. Si la app te dice que el método divergió, no te asustes: intenta cambiar tu valor inicial o revisa la Configuración Global.")

if __name__ == "__main__":
    inicio()