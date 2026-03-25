import plotly.graph_objects as go
import streamlit as st
import numpy as np
from core import utils as ut

@st.cache_data(show_spinner="Cargando trazado de la curva...")
def generar_base_fig(f, raiz, inf, sup,key=None):
    # Calculamos la distancia más larga desde la raíz a los extremos
    # para que al usarla en ambos lados, la raíz quede en el centro exacto.
    radio_vista = max(abs(raiz - inf), abs(raiz - sup))
    radio_con_margen = radio_vista * 1.1

    # Generamos los puntos basados en ese radio para que la curva no se corte
    x = np.linspace(raiz - radio_con_margen, raiz + radio_con_margen, 3000)
    y = ut.evaluar_f(f, x)
    
    fig = go.Figure()

    # Función f(x)
    fig.add_trace(go.Scatter(
        x=x, y=y, 
        mode='lines', 
        name='f(x)' if key!='grafico_pf' else 'g(x)', 
        line=dict(color='#1E88E5', width=3)
    ))
    if key == 'graf Punto Fijo':
        fig.add_trace(go.Scatter(
            x=x, y=x, # y = x
            mode='lines',
            name='y = x',
            line=dict(color='#FFCA28', width=2, dash='dash')
        ))
    elif key == 'graf_bis' or key == 'graf_sec':
        # Línea punteada para el límite inferior 'a'
        fig.add_vline(
            x=inf, 
            line_width=2, 
            line_dash="dash",
            line_color="rgba(30, 136, 229, 0.5)"
        )

        # Línea punteada para el límite superior 'b'
        fig.add_vline(
            x=sup, 
            line_width=2, 
            line_dash="dash", 
            line_color="rgba(30, 136, 229, 0.5)"
        )

    fig.update_layout(
        template='plotly_white',
        dragmode=False, 
        hovermode='x unified',
        margin=dict(l=40, r=40, t=100, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
        
        xaxis=dict(
            # Aplicamos el rango simétrico respecto a la raíz
            range=[raiz - radio_con_margen, raiz + radio_con_margen],
            # fixedrange=True,
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=True,
            zerolinecolor='rgba(176, 196, 222, 0.8)', 
            zerolinewidth=2.5
        ),
        yaxis=dict(
            range = [-max(abs(y))*1.2, max(abs(y))*1.2],
            # fixedrange=True,
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=True,
            zerolinecolor='rgba(176, 196, 222, 0.8)',
            zerolinewidth=2.5
        )
    )
    return fig

def generar_puntos_reg(fig,datos, raiz):
    fig_final = go.Figure(fig)

    x_puntos = datos['x']
    y_puntos = datos['y']
    
    fig_final.add_trace(go.Scatter(
        x=x_puntos,
        y=y_puntos,
        mode='markers',
        textposition="top center",
        name='Valores',
        marker=dict(symbol='x', size=10, color='#EF4444'),
        hovertemplate="Iteración %{text}: %{x:.6f}<extra></extra>"
    ))
    # Agregamos la Raíz final
    fig_final.add_trace(go.Scatter(
        x=[raiz], y=[0],
        mode='markers',
        name='Raíz',
        marker=dict(
            size=12, 
            color='#00E676', 
            line=dict(
                color='white', 
                width=2
                )
            )
    ))
    return fig_final

def generar_puntos_pf(f, fig, datos, raiz):
    
    fig_final = go.Figure(fig)
    
    if datos is not None and 'x[i]' in datos:
            # Convertimos a float por si vienen como strings desde la tabla
            x_puntos = [float(val) for val in datos['x[i]'][:-1]] 
            
            # En punto fijo, los puntos van sobre la curva g(x), en Newton sobre el eje X
            y_puntos = ut.evaluar_f(f, np.array(x_puntos))

            etiquetas = [f"x_{i}" for i in range(len(x_puntos))]
            fig_final.add_trace(go.Scatter(
                x=x_puntos,
                y=y_puntos,
                mode='markers',
                text=etiquetas,
                textposition="top center",
                name='Iteraciones x_i',
                marker=dict(symbol='x', size=10, color='#EF4444'),
                hovertemplate="Iteración %{text}: %{x:.6f}<extra></extra>"
            ))
        
    # Agregamos el punto final (La Raíz)
    # En Punto Fijo la intersección visual es en (raiz, raiz). En Newton es (raiz, 0).
    fig_final.add_trace(go.Scatter(
        x=[raiz], y=[raiz],
        mode='markers',
        name='Punto de Convergencia',
        marker=dict(
            size=12, 
            color='#00E676', 
            line=dict(color='white', width=2)
        )
    ))
    return fig_final

def generar_puntos(fig, datos, raiz):
    
    fig_final = go.Figure(fig)
    
    # Agregamos la "Telemetría" (las x rojas) solo si es necesario
    if datos is not None and 'x[i]' in datos:
        x_puntos = datos['x[i]'][:-1]
        etiquetas = [f"x_{i}" for i in range(len(x_puntos))]
        fig_final.add_trace(go.Scatter(
            x=x_puntos,
            y=[0] * len(x_puntos),
            mode='markers',
            text=etiquetas,
            textposition="top center",
            name='Rastro x_i',
            marker=dict(symbol='x', size=10, color='#EF4444'),
            hovertemplate="Iteración %{text}: %{x:.6f}<extra></extra>"
        ))
    # Agregamos la Raíz final
    fig_final.add_trace(go.Scatter(
        x=[raiz], y=[0],
        mode='markers',
        name='Raíz',
        marker=dict(
            size=12, 
            color='#00E676', 
            line=dict(
                color='white', 
                width=2
                )
            )
    ))
    
    return fig_final

def obtener_grafico(f, raiz, inf, sup, key=None, iteraciones=None):
    # Traemos la base del caché (instantáneo si no cambió f o el intervalo)
    fig = generar_base_fig(f, raiz, inf, sup,key)
    
    # Creamos una COPIA para no ensuciar el objeto original en el caché
    fig_final = go.Figure(fig)
    if key == 'graf Punto Fijo':
        fig_final = generar_puntos_pf(f,fig_final,iteraciones,raiz)
    elif key == 'regresion':
        fig_final = generar_puntos_reg(fig_final,iteraciones,raiz)
    else:
        fig_final = generar_puntos(fig_final,iteraciones,raiz)
    return fig_final

def dibujar(fig_final):  
    # Finalmente, mostramos el gráfico unificado
    st.plotly_chart(
        fig_final,
        width='stretch',
        config={
            'scrollZoom': False,
            'doubleClick': False, # <--- ESTO DESACTIVA EL RESET AL TOCAR
            'displayModeBar': True,
            'displaylogo': False,
            'showTips': False,
            'modeBarButtons': [[
                'zoomIn2d', 
                'zoomOut2d', 
                'resetViews'
                ]]
            }
        )

def renderizar_metrica_premium(titulo, valor_izq, valor_der, unidad="", invertido=False):
    # Renderiza una tarjeta HTML personalizada para comparar dos métricas.
    # invertido=True: Indica que un valor menor es MEJOR (ej: iteraciones).

    
    # Lógica para decidir quién ganó (verde) y quién perdió (rojo)
    if valor_izq == valor_der:
        color_izq, color_der = "#555", "#555" # Gris si son iguales
    else:
        # Si invertido es True, el menor gana
        ganador_izq = valor_izq < valor_der if invertido else valor_izq > valor_der
        color_izq = "#2ecc71" if ganador_izq else "#e74c3c" # Verde vs Rojo
        color_der = "#e74c3c" if ganador_izq else "#2ecc71" # Rojo vs Verde

    # Estilo CSS para la tarjeta
    st.markdown(f"""
    <style>
        .metric-card {{
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            text-align: center;
        }}
        .metric-title {{
            font-size: 0.9rem;
            color: #aaa;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        .metric-value-container {{
            display: flex;
            justify-content: space-around;
            align-items: baseline;
        }}
        .metric-value {{
            font-size: 1.8rem;
            font-weight: 700;
        }}
        .metric-unit {{
            font-size: 1rem;
            color: #777;
            margin-left: 5px;
        }}
        .vs-text {{
            font-size: 1rem;
            color: #555;
            font-weight: 800;
            margin: 0 10px;
        }}
    </style>
    
    <div class="metric-card">
        <div class="metric-title">{titulo.upper()}</div>
        <div class="metric-value-container">
            <div class="metric-value" style="color: #2E86C1;">{valor_izq}<span class="metric-unit">{unidad}</span></div>
            <div class="vs-text">vs</div>
            <div class="metric-value" style="color: #e74c3c;">{valor_der}<span class="metric-unit">{unidad}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def dibujar_batalla_errores(historial_izq, historial_der, nombre_izq, nombre_der):
    """
    Usa Plotly para dibujar el decaimiento del error de ambos métodos
    en escala logarítmica.
    """
    
    # Extraemos los errores absolutos de los diccionarios de Historial
    err_izq = historial_izq['Error Absoluto']
    err_der = historial_der['Error Absoluto']
    
    # Creamos los índices de iteraciones (X)
    iter_izq = list(range(1, len(err_izq) + 1))
    iter_der = list(range(1, len(err_der) + 1))

    # Creamos la figura de Plotly
    fig = go.Figure()

    # Traza Azul (Método Izquierdo)
    fig.add_trace(go.Scatter(
        x=iter_izq, 
        y=err_izq,
        mode='lines+markers',
        name=nombre_izq,
        line=dict(color='#2E86C1', width=3),
        marker=dict(size=6)
    ))

    # Traza Roja (Método Derecho)
    fig.add_trace(go.Scatter(
        x=iter_der, 
        y=err_der,
        mode='lines+markers',
        name=nombre_der,
        line=dict(color='#e74c3c', width=3, dash='dash'),
        marker=dict(size=6)
    ))

    # Configuración del Layout (Título, Ejes, Fondo transparente)
    fig.update_layout(
        title="Batalla de Convergencia: Decaimiento del Error",
        xaxis_title="Número de Iteración",
        yaxis_title="Error Absoluto (Tolerancia)",
        yaxis_type="log", # <-- Escala logarítmica
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        hovermode="x unified", # Muestra ambos valores al pasar el mouse
        dragmode=False
    )
    
    # Cuadrícula suave
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)')

    # Renderizamos en Streamlit
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            'scrollZoom': False,
            'doubleClick': False, # <--- ESTO DESACTIVA EL RESET AL TOCAR
            'displayModeBar': False,
            'displaylogo': False,
            'showTips': False,
            'modeBarButtons': [[
                'zoomIn2d', 
                'zoomOut2d', 
                'resetViews'
                ]]
            }
        )

def dibujar_radar_veredicto(nombre_izq, scores_izq, nombre_der, scores_der):

    # Usa Plotly Scatterpolar para dibujar un gráfico de araña comparando múltiples categorías normalizadas (0-10).

    # Categorías para los ejes
    categorias = ['VELOCIDAD\n(Tiempo/Iters)', 'EFICIENCIA DE COSTO\n(Menos Cálculos)', 'ROBUSTEZ\n(Garantía Conv)']
    
    # El gráfico Scatterpolar de Plotly requiere "cerrar" el círculo
    # repitiendo el primer puntaje al final.
    scores_izq_cerrado = scores_izq + [scores_izq[0]]
    scores_der_cerrado = scores_der + [scores_der[0]]
    categorias_cerrado = categorias + [categorias[0]]

    fig = go.Figure()

    # Traza Azul (Método Izquierdo)
    fig.add_trace(go.Scatterpolar(
        r=scores_izq_cerrado,
        theta=categorias_cerrado,
        fill='toself', # Relleno de área
        name=nombre_izq,
        line=dict(color='#2E86C1', width=3),
        marker=dict(size=6)
    ))

    # Traza Roja (Método Derecho)
    fig.add_trace(go.Scatterpolar(
        r=scores_der_cerrado,
        theta=categorias_cerrado,
        fill='toself', # Relleno de área
        name=nombre_der,
        line=dict(color='#e74c3c', width=3, dash='dash'), 
        marker=dict(size=6)
    ))

    # Configuración del Layout "Mobile-Friendly"
    fig.update_layout(
        title=dict(
            text="🏆 Veredicto de Batalla",
            font=dict(size=16) # Achicamos un pelín el título
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color="gray", size=10) # Achicamos los numeritos
            ),
            angularaxis=dict(
                tickfont=dict(color="white", size=11), # Achicamos los textos de las puntas
                gridcolor='rgba(255,255,255,0.1)'
            ),
            bgcolor='rgba(0,0,0,0)' 
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        
        legend=dict(
            orientation="h",       # Horizontal
            yanchor="top", y=-0.2, # La tiramos abajo del gráfico
            xanchor="center", x=0.5 # Bien centrada
        ),
        
        # (l=left, r=right, t=top, b=bottom)
        margin=dict(l=25, r=25, t=40, b=20),
        
        # FORZAR ALTURA MÍNIMA (Para que no se achiche)
        height=350 
    )
    
    # Renderizamos en Streamlit
    st.plotly_chart(fig, width='stretch', config={'staticPlot': True})