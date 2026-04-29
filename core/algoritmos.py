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

def regula_falsi(f,a,b,err):

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

def newton(f,x_0,err):

    max_iters = st.session_state.get('max_iters',100)
    cero_maquina = st.session_state.get('cero_maquina', 1e-12)
    limite_infinito = st.session_state.get('limite_infinito', 1e6)
    tipo_err = st.session_state.get('tipo_error', 'Absoluto')
    datos = Historial({'x[i]','f(x[i])',"f'(x[i])",'x[i+1]',f'Error {tipo_err}'})

    # Variables útiles
    x_n=x_0
    iteracion=0
    derivada = str(sp.diff(f, 'x'))

    # Cálculo de la raíz
    while iteracion < max_iters:
        fa = ut.evaluar_f(f, x_n)
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

def punto_fijo(g,x_0,err):

    max_iters = st.session_state.get('max_iters',100)
    cero_maquina = st.session_state.get('cero_maquina', 1e-12)
    limite_infinito = st.session_state.get('limite_infinito', 1e6)
    tipo_err = st.session_state.get('tipo_error', 'Absoluto')
    datos = Historial(['x[i]','g(x[i])',f'Error {tipo_err}'])

    # Variables útiles
    x_n=x_0
    iteracion=0

    # Cálculo de la raíz
    while iteracion < max_iters:
        try:
            x_n1 = ut.evaluar_f(g, x_n)
            err_cal = ut.calcular_error(x_n1, x_n)

            datos.agregar({
            'x[i]':x_n,
            'g(x[i])':x_n1,
            f'Error {tipo_err}':err_cal
            })

            # Condiciones de corte
            if err_cal > limite_infinito:
                return None, datos  # Divergió (devuelve None)

            if err_cal <= err:
                return x_n1, datos  # Convergió (devuelve la raíz)

            x_n = x_n1

        except Exception:
            return None, datos # Explotó la matemática

        iteracion+=1

    return None, datos # Llegó al límite de iteraciones sin converger

def secante(f,x_n1,x_n,err):

    max_iters = st.session_state.get('max_iters',100)
    cero_maquina = st.session_state.get('cero_maquina', 1e-12)
    limite_infinito = st.session_state.get('limite_infinito', 1e6)
    tipo_err = st.session_state.get('tipo_error', 'Absoluto')
    datos = Historial({'x[i]','f(x[i])',"dx[i]",'x[i+1]',f'Error {tipo_err}'})

    iteracion = 0
    while iteracion < max_iters:

        try:
            fx_n = ut.evaluar_f(f,x_n)
            fx_n1 = ut.evaluar_f(f,x_n1)

            x = x_n - fx_n * ((x_n - x_n1)/(fx_n - fx_n1))
            fx = ut.evaluar_f(f,x)

            err_cal = ut.calcular_error(x_n1, x_n)


            # Guardamos los datos de esta vuelta en el cuadro
            datos.agregar({
                'x[i]':x_n,
                'f(x[i])':fx,
                "dx[i]":x_n1 - x_n,
                'x[i+1]':x_n1,
                f'Error {tipo_err}':err_cal
                })

            if abs(fx) < cero_maquina:
                return x, datos

            if abs(x_n1) > limite_infinito:
                return None, datos

            if err_cal <= err:
                return x, datos

            else:
                x_n, x_n1 = x, x_n

            iteracion+=1

        except ZeroDivisionError:
            print("División por 0. Probar con otros valores.")
            return None, datos

def regresion(x_vals, y_vals):
    """
    Recibe listas normales de Python. Devuelve la pendiente (m),
    ordenada al origen (b), la raíz, el R^2 y la instancia de Historial, datos.
    """
    datos = Historial(['x', 'y'])

    if len(x_vals) < 2 or len(x_vals) != len(y_vals):
        return None, None, None, None, datos

    try:
        m, b = statistics.linear_regression(x_vals, y_vals)
        r = statistics.correlation(x_vals, y_vals)
        r2 = r ** 2
        raiz = -b / m if m != 0 else None

        for x, y in zip(x_vals, y_vals):
            datos.agregar({'x': x, 'y': y})

        return m, b, raiz, r2, datos

    except Exception:
        return None, None, None, None, datos

