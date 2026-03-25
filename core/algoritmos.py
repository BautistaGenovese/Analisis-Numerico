from core.historial import Historial
from core import utils as ut
import streamlit as st
import sympy as sp
import statistics

@st.cache_data(show_spinner="Calculando telemetría...")
def biseccion(f,a,b,err):
    
    datos = Historial(['a[i]','b[i]','x[i]','f(x[i])','Dx[i]','Error Absoluto'])
    
    fa = ut.evaluar_f(f,a)
    fb = ut.evaluar_f(f,b)

    # Casos base
    if fa * fb >= 0:
        return None, datos
    if a > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Calculo de la raíz
    x_anterior=a
    iteracion=0
    while iteracion < 100:
        
        x=(a+b)/2
        fx=ut.evaluar_f(f,x)
        err_abs = abs(b-a)/2
        
        datos.agregar({
            'a[i]':a,
            'b[i]':b,
            'x[i]':x,
            'f(x[i])':fx,
            'Dx[i]':(x-a),
            'Error Absoluto':err_abs
        })

        # Frena cuando el resultado es demasiado cercano al cero
        if abs(fx) < 1e-12: 
            return x, datos
            
        # Cierra el ciclo cuando la diferencia entre cada iteración es minima
        if abs(x - x_anterior) < err:
            break
        
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
        
        x_anterior=x
        iteracion+=1

    return x, datos

@st.cache_data(show_spinner="Calculando telemetría...")
def secante(f,a,b,err):
    
    datos = Historial(['a[i]','b[i]','x[i]','f(x[i])','Dx[i]','Error Absoluto'])
    
    fa = ut.evaluar_f(f,a)
    fb = ut.evaluar_f(f,b)

    # Casos base
    if fa * fb >= 0:
        return None, datos.obtener_datos()
    if a  > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Calculo de la raíz
    x_anterior=a
    iteracion=0
    while iteracion < 100:
        
        # Frena si es que la diferencia entre las derivadas es cercana al cero
        if abs(fb - fa) < 1e-12:
            st.warning("División por cero en secante. Los puntos están muy cerca.")
            return None, datos
        
        x = b - (fb * (b - a)) / (fb - fa)
        fx = ut.evaluar_f(f, x)
        err_abs = abs(b - a)

        datos.agregar({
            'a[i]':a,
            'b[i]':b,
            'x[i]':x,
            'f(x[i])':fx,
            'Dx[i]':(x-a),
            'Error Absoluto':err_abs
        })
        
        # Frena cuando el resultado es demasiado cercano al cero
        if abs(fx) < 1e-12: 
            return x, datos
            
        # Cierra el ciclo cuando la diferencia entre cada iteración es minima
        if abs(x - x_anterior) < err:
            break
        
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
        
        x_anterior=x
        iteracion+=1
        
    return x, datos

@st.cache_data(show_spinner="Calculando telemetría...")
def newton(x_n,f,err):
   # Creamos el diccionario para guardar las iteraciones
    datos = Historial({'x[i]','f(x[i])',"f'(x[i])",'x[i+1]','Error Absoluto'})
    
    iteracion=0
    while iteracion < 100:
        fa = ut.evaluar_f(f, x_n)
        derivada = str(sp.diff(f, 'x'))
        d_evaluada = round(ut.evaluar_f(derivada, x_n), 6)
        
        # Evitamos la división por cero si la derivada da 0
        if d_evaluada == 0:
            return None, datos
            
        x_n1 = x_n - (fa / d_evaluada)
        
        err_abs = abs(x_n1 - x_n)

        # Guardamos los datos de esta vuelta en el cuadro
        datos.agregar({
            'x[i]':x_n,
            'f(x[i])':fa,
            "f'(x[i])":d_evaluada,
            'x[i+1]':x_n1,
            'Error Absoluto':err_abs
            })

        # Condición de corte
        if abs(ut.evaluar_f(f, x_n1)) <= 1e-12:
            return x_n1, datos
        
        # Condición de corte por si se estanca
        if abs(x_n1 - x_n) <= err:
            return x_n1, datos
        
        x_n=x_n1
        iteracion+=1

@st.cache_data(show_spinner=True)
def punto_fijo (g,x0, err):
   
    datos = Historial(['x[i]','g(x[i])','Error Absoluto'])
    
    x_actual=x0
    iteracion=0
    while iteracion < 100:
        try:
            x_nuevo = ut.evaluar_f(g, x_actual)
            err_abs = abs(x_nuevo - x_actual)
            
            datos.agregar({
            'x[i]':x_actual,
            'g(x[i])':x_nuevo,
            'Error Absoluto':err_abs
            })
            
            # Sale si el error absoluto es demasiado grande
            if err_abs > 1e6:
                return x_nuevo, datos, False
            
            # |x_(i+1) - x_i| <= ε
            if err_abs <= err:
                
                return x_nuevo, datos, True
            
            x_actual = x_nuevo
            
        except Exception:
            return None, datos, False
        
        iteracion+=1        
    return x_actual, datos, False

@st.cache_data(show_spinner=True)
def calcular_regresion(x_vals, y_vals):
    """
    Recibe listas normales de Python. Devuelve la pendiente (m), 
    ordenada al origen (b), la raíz y el R^2.
    """
    if len(x_vals) < 2 or len(x_vals) != len(y_vals):
        return None, None, None, None

    try:
        # Calculamos la recta
        m, b = statistics.linear_regression(x_vals, y_vals)
        
        # Calculamos qué tan bueno es el ajuste (R cuadrado)
        r = statistics.correlation(x_vals, y_vals)
        r2 = r ** 2
        
        raiz = None
        if m != 0:
            raiz = -b / m  # Despejamos X cuando Y = 0
            
        return m, b, raiz, r2
    except Exception:
        return None, None, None, None

