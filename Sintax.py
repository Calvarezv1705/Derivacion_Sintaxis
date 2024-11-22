import tkinter as tk  # Importa tkinter para crear la interfaz gráfica.
from tkinter import ttk, messagebox  # Importa widgets adicionales como combobox y cuadros de mensajes.
from nltk import CFG, ChartParser, Tree  # Importa herramientas para gramáticas y árboles de derivación.
import re  # Importa la biblioteca para manejar expresiones regulares.

# Define la gramática que describe cómo se forman las expresiones matemáticas.
GRAMATICA = CFG.fromstring("""
    E -> E '+' T | E '-' T | T
    T -> T '*' F | T '/' F | F
    F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
""")

# Crea el parser (analizador sintáctico) basado en la gramática definida.
PARSER = ChartParser(GRAMATICA)

# Clase que maneja la lógica de derivación y generación de árboles.
class Derivacion:
    def __init__(self, parser):
        self.parser = parser

    # Función para separar una expresión matemática en sus componentes (tokens).
    def separarTokens(self, expresion):
        # Usa expresiones regulares para encontrar números, letras, operadores y paréntesis.
        return re.findall(r'\d+|[a-z]+|[+\-*/()]', expresion)

    # Función para derivar la expresión usando una estrategia por izquierda.
    def derivacionIzquierda(self, expresion):
        pasos = []  # Lista para guardar los pasos de derivación.
        arboles = []  # Lista para guardar los árboles generados.
        for tree in self.parser.parse(expresion):  # Genera los árboles de derivación.
            pasos.append(tree.productions())  # Almacena las producciones (reglas aplicadas).
            arboles.append(tree)  # Guarda el árbol generado.
            break 
        return pasos, arboles  # Devuelve los pasos y árboles.

    # Función para derivar la expresión usando una estrategia por derecha.
    def derivacionDerecha(self, expresion):
        pasos = []  # Lista para guardar los pasos de derivación.
        arboles = []  # Lista para guardar los árboles generados.
        for tree in self.parser.parse(expresion):  # Genera los árboles de derivación.
            pasosDer = tree.productions()[::-1]  # Invierte el orden de las producciones.
            pasos.append(pasosDer)  # Almacena las producciones invertidas.
            arboles.append(tree)  # Guarda el árbol generado.
            break 
        return pasos, arboles  # Devuelve los pasos y árboles.

    # Función para generar el Árbol Sintáctico Abstracto (AST).
    def crearAST(self, arbol):
        if arbol.height() <= 2:  # Si el árbol tiene altura <= 2, es un nodo hoja.
            return arbol
        elif arbol.label() in ["E", "T", "F"]:  # Si el nodo es E, T o F.
            # Aplica recursión para procesar los hijos del nodo.
            return Tree(arbol.label(), [self.crearAST(hijo) for hijo in arbol if isinstance(hijo, Tree)])
        return arbol  # Retorna el árbol simplificado.

# Clase que define la interfaz gráfica y su lógica.
class AplicacionDerivacion:
    def __init__(self, root): # El método __init__ inicializa los atributos 'nombre' y 'edad' cuando se crea una nueva instancia de Persona.

        self.root = root  # Guarda la ventana principal (pasada como argumento al crear la clase).
        self.root.title("Generador de Árboles de Derivación y AST")  # Establece el título de la ventana.
        self.root.geometry("600x500")  # Define el tamaño inicial de la ventana.

        self.derivacion = Derivacion(PARSER)  # Crea una instancia de la clase Derivacion.

        # Etiqueta para la entrada de la expresión.
        # Agrega un texto que dice "Expresión:".
        tk.Label(root, text="Expresión:").pack(pady=5)  

        self.expresionInput = tk.Entry(root, width=50)  # Crea un cuadro de texto donde el usuario puede escribir.
        self.expresionInput.pack(pady=5)  # Coloca el cuadro de texto en la ventana con un poco de espacio vertical.

        # Etiqueta para seleccionar el tipo de derivación.
        # Agrega un texto que dice "Tipo de derivación:".
        tk.Label(root, text="Tipo de derivación:").pack(pady=5)  

        # Combobox para elegir entre derivación por izquierda o derecha.
        self.tipoDerivacion = ttk.Combobox(root, values=["Izquierda", "Derecha"], state="readonly", width=20) 
        
        self.tipoDerivacion.pack(pady=5)  # Coloca el combobox en la ventana.
        self.tipoDerivacion.set("Izquierda")  # Selecciona "Izquierda" como valor predeterminado.

        # Botón para generar la derivación y los árboles.
        tk.Button(root, text="Generar Árboles", command=self.Output).pack(pady=10)  
        
        # Cuadro de texto para mostrar los pasos de derivación.
        self.textoOutPut = tk.Text(root, wrap=tk.WORD, height=20, width=70, state=tk.DISABLED)  
        
        self.textoOutPut.pack(pady=10)  # Coloca el cuadro de texto en la ventana.

    # Método que maneja la generación de derivaciones y árboles.
    def Output(self):
        expression = self.expresionInput.get().strip()  # Obtiene el texto del cuadro de entrada y elimina espacios.
        tipoDerivacion = self.tipoDerivacion.get()  # Obtiene el tipo de derivación

        if not expression:  # Si no se ingresó nada en el cuadro de entrada:
            messagebox.showerror("Error", "Por favor, ingrese una expresión.")  
            return

        try:
            tokens = self.derivacion.separarTokens(expression)  # Separa la expresión ingresada en partes

            # Genera las derivaciones según el tipo seleccionado.
            if tipoDerivacion == "Izquierda":  
                pasosDerivacion, trees = self.derivacion.derivacionIzquierda(tokens)
            else:  
                pasosDerivacion, trees = self.derivacion.derivacionDerecha(tokens)

            if not pasosDerivacion:  # Si no se generaron derivaciones:
                messagebox.showerror("Error", "No se pudo generar ninguna derivación para la expresión ingresada.")  
                return

            # Limpia el cuadro de texto y muestra los pasos.
            self.textoOutPut.config(state=tk.NORMAL)  # Habilita el cuadro de texto para editar.
            self.textoOutPut.delete(1.0, tk.END)  # Borra todo el contenido del cuadro de texto.

            self.textoOutPut.insert(tk.END, "Derivación Paso a Paso:\n") # Inserta un título para los pasos de derivación.

            for step in pasosDerivacion:  # Recorre cada paso de la derivación:
                for production in step:  # Recorre las reglas usadas en ese paso:
                    self.textoOutPut.insert(tk.END, f"  {production}\n")  # Muestra cada regla aplicada.
                self.textoOutPut.insert(tk.END, "\n")  # Agrega un espacio entre pasos.

            # Muestra los árboles generados.
            for tree_index, tree in enumerate(trees, start=1):  # Recorre los árboles generados:
                tree.draw()  # Dibuja el árbol de derivación en una ventana aparte.
                ast = self.derivacion.crearAST(tree)  # Genera un Árbol Sintáctico Abstracto (AST) a partir del árbol.
                ast.draw()  # Dibuja el AST en otra ventana aparte.

            self.textoOutPut.config(state=tk.DISABLED)  # Deshabilita el cuadro de texto (solo lectura).

        except Exception as e:  # Si ocurre algún error durante el proceso:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")  
            # Muestra un mensaje de error con información sobre lo ocurrido.

# Código principal para ejecutar la aplicación.
if __name__ == "__main__":  # Verifica que el archivo se está ejecutando directamente.
    root = tk.Tk()  # Crea la ventana principal de la aplicación.
    app = AplicacionDerivacion(root)  # Crea una instancia de la clase AplicacionDerivacion.
    root.mainloop()  # Inicia el bucle principal para mantener la ventana abierta.