import streamlit as st
from metodos.metodo_numerico import MetodoNumerico
from core.algoritmos import punto_fijo
from core import utils as ut

class PuntoFijo(MetodoNumerico):
    
    @property
    def nombre(self): return "Punto Fijo"
    
    def ejecutar(self, f, err, **params):
        raiz, datos = punto_fijo(
            g=f,
            x_0=params['x_0'],
            err=err
            )
        
        # Si la raíz es compleja, el método divergió → tratarlo como None
        if raiz is not None and isinstance(raiz, complex):
            return None, datos
        
        return raiz, datos

    def render_teoria(self):
        with st.expander("📖 ¿Cómo funciona el método de Punto Fijo?"):
            st.markdown("""
            **Concepto básico:** Este método transforma la ecuación original de búsqueda de raíces $f(x) = 0$ en una ecuación equivalente de la forma $x = g(x)$. Se toma un valor inicial, se evalúa en $g(x)$, y el resultado se convierte en la entrada para la siguiente iteración. Visualmente, buscamos el punto donde la curva $g(x)$ se cruza con la recta $y = x$.
            
            **Fórmula de iteración:**
            """)
            st.latex(r"x_{i+1} = g(x_i)")
            
            st.markdown("""
            **Intervalos permitidos y Condiciones:**
            * Requiere **un valor inicial** $x_0$.
            * Debes ser capaz de despejar una $x$ de tu función original $f(x)$ para crear $g(x)$.
            """)
            st.info(r"💡 **Criterio de Convergencia:** Para que el método no diverja hacia el infinito, la curva de $g(x)$ debe ser 'suave' cerca de la raíz. Matemáticamente, el valor absoluto de su derivada debe ser menor a 1: $|g'(x)| < 1$.")
    
    def render_formula(self, valor_default=None):
        
        modo = st.radio(
            "¿Cómo deseas ingresar la función?",
            
            [
                "Ingresar g(x) despejada (Recomendado)",
                "Generar g(x) automáticamente a partir de f(x)"
             ],
            
            help="El método automático usa la transformación trivial g(x) = x - f(x), pero suele divergir con facilidad."
        )
            
        if modo == "Ingresar g(x) despejada (Recomendado)":
            g = st.text_input('Escribe tu función despejada $g(x)$:', value='(x + 2)**(0.5)')
            st.latex('g(x)' + ut.mostrar_formula(g)[4:])
        else:
            
            f = st.text_input('Escribe tu función original $f(x)$:', value='x**2 - x - 2')
            st.caption("Transformación aplicada: $g(x) = x - f(x)$")
            st.latex(ut.mostrar_formula(f))
            
            # Generamos automáticamente el string de la nueva función g(x)
            g = f"x - ({f})"
            st.latex(f"g(x) = x - ({ut.mostrar_formula(f)[7:]})") # Mostramos cómo quedó
        
        exponente_err = st.select_slider(
            "Presición",
            options=[1,2,3,4,5,6,7,8,9,10],
            value=2,
            format_func=lambda x: f"$10^{{{-int(x)}}}$"
            )
        # Por ejemplo: 10^(-2)
        err = 10**(-exponente_err)
        
        return g, err, exponente_err
    
    def render_inputs(self,key=None):
        x_0 = st.number_input('Ingresar $(x_0)$',value=0.0,step=2.0,key=key)
        return {'x_0':x_0}
    
    def mostrar_codigo(self):
        st.code('''
def punto_fijo (x0, err):
    
    x_actual=x0
    iteracion=0
    while iteracion < 100:
        try:
            x_nuevo = g(x_actual)
            # |x_(i+1) - x_i|
            error_abs = abs(x_nuevo - x_actual)

            # Sale si el error absoluto es demasiado grande
            if error_abs > 1e6:
                return x_nuevo
            
            # |x_(i+1) - x_i| <= ε
            if error_abs <= err:
                return x_nuevo
            
            x_actual = x_nuevo
            
        except Exception:
            return None
        iteracion+=1  
                 
    return x_actual
    ''', "python") 
    
    def get_rango_grafico(self, raiz, **params):
        return raiz-5, raiz+5

if __name__ == "__main__":
    app = PuntoFijo()
    app.mostrar_info()