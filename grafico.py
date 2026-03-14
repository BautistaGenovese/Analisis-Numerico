import plotly.graph_objects as go
import streamlit as st
import numpy as np
import utils as ec

@st.cache_data(show_spinner="Cargando trazado de la curva...")
def generar_base_fig(f, raiz, inf, sup,key=None):
    # Calculamos la distancia más larga desde la raíz a los extremos
    # para que al usarla en ambos lados, la raíz quede en el centro exacto.
    radio_vista = max(abs(raiz - inf), abs(raiz - sup))
    radio_con_margen = radio_vista * 1.1

    # Generamos los puntos basados en ese radio para que la curva no se corte
    x = np.linspace(raiz - radio_con_margen, raiz + radio_con_margen, 1000)
    y = ec.evaluar_f(f, x)
    
    fig = go.Figure()

    # Función f(x)
    fig.add_trace(go.Scatter(
        x=x, y=y, 
        mode='lines', 
        name='f(x)', 
        line=dict(color='#1E88E5', width=3)
    ))
    if key == 'grafico_pf':
        fig.add_trace(go.Scatter(
            x=x, y=x, # y = x
            mode='lines',
            name='y = x',
            line=dict(color='#FFCA28', width=2, dash='dash')
        ))
    elif key != 'regresion':
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
            y_puntos = ec.evaluar_f(f, np.array(x_puntos))

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

def generar_puntos(f, fig, datos, raiz):
    
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

def dibujar(f, raiz, inf, sup, key=None, iteraciones=None):
    # Traemos la base del caché (instantáneo si no cambió f o el intervalo)
    fig = generar_base_fig(f, raiz, inf, sup,key)
    
    # Creamos una COPIA para no ensuciar el objeto original en el caché
    fig_final = go.Figure(fig)
    if key == 'grafico_pf':
        fig_final = generar_puntos_pf(f,fig_final,iteraciones,raiz)
    elif key == 'regresion':
        fig_final = generar_puntos_reg(fig_final,iteraciones,raiz)
    else:
        fig_final = generar_puntos(f,fig_final,iteraciones,raiz)
        
    # Finalmente, mostramos el gráfico unificado
    st.plotly_chart(
        fig_final,
        use_container_width=True,
        key=key,
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
