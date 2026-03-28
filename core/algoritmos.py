from core.historial import Historial
from core import utils as ut
import streamlit as st
import sympy as sp
import statistics

def biseccion(f,a,b,err):
    
    fa = ut.evaluar_f(f,a)
    fb = ut.evaluar_f(f,b)
    
    max_iters = st.session_state.get('max_iters',100)
    cero_maquina = st.session_state.get('cero_maquina', 1e-12)
    tipo_err = st.session_state.get('tipo_error', 'Absoluto')
    datos = Historial(['a[i]','b[i]','x[i]','f(x[i])','Dx[i]',f'Error {tipo_err}'])

    # Casos base
    if fa * fb >= 0:
        return None, datos
    if a > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Variables útiles
    x_anterior=a
    iteracion=0
    
    # Calculo de la raíz
    while iteracion < max_iters:
        
        x=(a+b)/2
        fx=ut.evaluar_f(f,x)
        # Ignora la iteración 0 para el relativo
        if iteracion > 0:
            err_cal = ut.calcular_error(x, x_anterior)
        else:
            err_cal = abs(b - a) / 2 # Error clásico inicial
        
        datos.agregar({
            'a[i]':a,
            'b[i]':b,
            'x[i]':x,
            'f(x[i])':fx,
            'Dx[i]':(x-a),
            f'Error {tipo_err}':err_cal
        })

        # Frena cuando el resultado es demasiado cercano al cero
        if abs(fx) < cero_maquina: 
            return x, datos
            
        # Cierra el ciclo cuando la diferencia entre cada iteración es minima
        if err_cal < err and iteracion > 0:
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

def secante(f,a,b,err):
    
    fa = ut.evaluar_f(f,a)
    fb = ut.evaluar_f(f,b)
    
    max_iters = st.session_state.get('max_iters',100)
    cero_maquina = st.session_state.get('cero_maquina', 1e-12)
    tipo_err = st.session_state.get('tipo_error', 'Absoluto')
    datos = Historial(['a[i]','b[i]','x[i]','f(x[i])','Dx[i]',f'Error {tipo_err}'])

    # Casos base
    if fa * fb >= 0:
        return None, datos
    if a  > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Variables útiles
    x_anterior=a
    iteracion=0
    
    # Calculo de la raíz
    while iteracion < max_iters:
        
        # Frena si es que la diferencia entre las derivadas es cercana al cero
        if abs(fb - fa) < cero_maquina:
            st.warning("División por cero en secante. Los puntos están muy cerca.")
            return None, datos
        
        x = b - (fb * (b - a)) / (fb - fa)
        fx = ut.evaluar_f(f, x)
        err_cal = ut.calcular_error(x, x_anterior)

        datos.agregar({
            'a[i]':a,
            'b[i]':b,
            'x[i]':x,
            'f(x[i])':fx,
            'Dx[i]':(x-a),
            f'Error {tipo_err}':err_cal
        })
        
        # Condiciones de corte 
        if abs(fx) < cero_maquina: 
            return x, datos
            
        if err_cal < err:
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

def newton(x_n,f,err):
    
    max_iters = st.session_state.get('max_iters',100)
    cero_maquina = st.session_state.get('cero_maquina', 1e-12)
    limite_infinito = st.session_state.get('limite_infinito', 1e-12)
    tipo_err = st.session_state.get('tipo_error', 'Absoluto')
    datos = Historial({'x[i]','f(x[i])',"f'(x[i])",'x[i+1]',f'Error {tipo_err}'})
    
    # Variables útiles
    iteracion=0
    
    # Cálculo de la raíz
    while iteracion < max_iters:
        fa = ut.evaluar_f(f, x_n)
        derivada = str(sp.diff(f, 'x'))
        d_evaluada = ut.evaluar_f(derivada, x_n)
        
        # Evitamos la división por cero si la derivada da 0
        if d_evaluada == 0:
            return None, datos
            
        x_n1 = x_n - (fa / d_evaluada)
        err_cal = ut.calcular_error(x_n1, x_n)


        # Guardamos los datos de esta vuelta en el cuadro
        datos.agregar({
            'x[i]':x_n,
            'f(x[i])':fa,
            "f'(x[i])":d_evaluada,
            'x[i+1]':x_n1,
            f'Error {tipo_err}':err_cal
            })

        # Condiciones de corte
        if abs(x_n1) > limite_infinito:
            return None, datos
        
        if abs(ut.evaluar_f(f, x_n1)) <= cero_maquina:
            return x_n1, datos
        
        if err_cal <= err:
            return x_n1, datos
        
        x_n=x_n1
        iteracion+=1

def punto_fijo (g,x0, err):
    
    max_iters = st.session_state.get('max_iters',100)
    cero_maquina = st.session_state.get('cero_maquina', 1e-12)
    limite_infinito = st.session_state.get('limite_infinito', 1e-12)
    tipo_err = st.session_state.get('tipo_error', 'Absoluto')
    datos = Historial(['x[i]','g(x[i])',f'Error {tipo_err}'])
    
    # Variables útiles
    x_actual=x0
    iteracion=0
    
    # Cálculo de la raíz
    while iteracion < max_iters:
        try:
            x_nuevo = ut.evaluar_f(g, x_actual)
            err_cal = ut.calcular_error(x_nuevo, x_actual)
            
            datos.agregar({
            'x[i]':x_actual,
            'g(x[i])':x_nuevo,
            f'Error {tipo_err}':err_cal
            })
    
            # Condiciones de corte
            if err_cal > limite_infinito:
                return None, datos  # Divergió (devuelve None)

            if err_cal <= err:
                return x_nuevo, datos  # Convergió (devuelve la raíz)
            
            x_actual = x_nuevo
            
        except Exception:
            return None, datos # Explotó la matemática
        
        iteracion+=1        
        
    return None, datos # Llegó al límite de iteraciones sin converger

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

