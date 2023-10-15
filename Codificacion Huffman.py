#Codificacion Huffman 
import math
import heapq
from collections import defaultdict, Counter

def leer_archivo():  
    with open('ejemplo1.txt', 'r', encoding='utf-8') as archivo:   # with para abrir un archivo llamado 'ejemplo1.txt' en modo de lectura ('r') y se especifica que el archivo está codificado en UTF-8archivo se utiliza como un alias para el archivo abierto.
        contenido = archivo.read() # lee todo el contenido del archivo abierto (archivo) y lo almacena en la variable contenido
    return contenido

def contar_caracteres_individuales():
    "Retorna un diccionario donde las keys son el símbolo y Value es su frecuencia de aparición"
    texto = leer_archivo()  
    diccionario = {}
    for caracter in texto:
        if caracter not in diccionario:
            diccionario[caracter] = 1
        else:
            num = diccionario[caracter]
            diccionario[caracter] = num + 1
    return diccionario

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construir_arbol_huffman(frecuencias):
    cola_prioridad = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
    heapq.heapify(cola_prioridad)
    
    while len(cola_prioridad) > 1:
        izquierda = heapq.heappop(cola_prioridad)
        derecha = heapq.heappop(cola_prioridad)
        nuevo_nodo = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
        nuevo_nodo.izquierda = izquierda
        nuevo_nodo.derecha = derecha
        heapq.heappush(cola_prioridad, nuevo_nodo)
    
    return cola_prioridad[0]

def construir_tabla_codificacion(arbol_huffman, ruta='', tabla_codificacion=None):
    if tabla_codificacion is None:
        tabla_codificacion = {}
    
    if arbol_huffman.caracter is not None:
        tabla_codificacion[arbol_huffman.caracter] = ruta
    if arbol_huffman.izquierda is not None:
        construir_tabla_codificacion(arbol_huffman.izquierda, ruta + '0', tabla_codificacion)
    if arbol_huffman.derecha is not None:
        construir_tabla_codificacion(arbol_huffman.derecha, ruta + '1', tabla_codificacion)
    
    return tabla_codificacion

def codificar_texto(texto, tabla_codificacion):
    bits = ''
    for caracter in texto:
        bits += tabla_codificacion[caracter]
    return bits

def decodificar_texto(bits, arbol_huffman):
    texto_decodificado = ''
    nodo_actual = arbol_huffman
    for bit in bits:
        if bit == '0':
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        
        if nodo_actual.caracter is not None:
            texto_decodificado += nodo_actual.caracter
            nodo_actual = arbol_huffman
    
    return texto_decodificado

#Funcion que recibe un archivo de texto y retorna una cadena
def leer_archivo():
    with open('ejemplo1.txt', 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    return contenido

#Funcion para calcular el numero de caracteres que hay en el texto
def contar_caracteres():
    texto = leer_archivo()  # Utilizar el nombre de la función de lectura
    return len(texto)

def calcular_longitud_texto(texto):
    # Función para calcular la longitud del texto en bits
    return len(''.join(format(ord(char), '08b') for char in texto))

def punto_1_huffman():
    print("Codificacion Huffman ") 
    if __name__ == '__main__':
       texto = leer_archivo()

       #numero de veces que se repiten los caracteres individuales en el texto 
       frecuencias = dict(Counter(texto)) 
       arbol_huffman = construir_arbol_huffman(frecuencias)
       tabla_codificacion = construir_tabla_codificacion(arbol_huffman)#apartir del arbol de hufman se asigna 0 a la izquierda y 1 a la derecha    
       texto_codificado = codificar_texto(texto, tabla_codificacion)
       print("Texto codificado:", texto_codificado)
    
       texto_decodificado = decodificar_texto(texto_codificado, arbol_huffman)
       print("Texto decodificado:", texto_decodificado)
    
    # Texto original
    texto_original = texto

     #  Calcula la longitud del texto original en bits
    longitud_original = calcular_longitud_texto(texto_original)

    # Codificar el texto original
    texto_codificado = codificar_texto(texto_original, tabla_codificacion)

     # Calcula la longitud del texto comprimido en bits
    longitud_comprimida = len(texto_codificado)

    # Calcula la eficiencia
    eficiencia = longitud_original / longitud_comprimida

     # Calcula la redundancia
    redundancia = 1 - eficiencia

     # Calcula la tasa de compresión
    tasa_compresion = ((longitud_original - longitud_comprimida) / longitud_original) * 100

    print("Longitud del texto original en bits:", longitud_original)
    print("Longitud del texto comprimido en bits:", longitud_comprimida)
    print("Eficiencia:", eficiencia)
    print("Redundancia:", redundancia)
    print("Tasa de compresión:", tasa_compresion, "%","\n \n ")


#__________________________________________________________________________________________________________________________
#punto 2  digrama

# Función para contar los bigramas
def contar_bigramas(texto):
    bigramas = {}
    for i in range(len(texto) - 1):
        bigrama = texto[i:i + 2]
        if bigrama in bigramas:
            bigramas[bigrama] += 1
        else:
            bigramas[bigrama] = 1
    return bigramas

def contar_bits_necesarios(numero):
    # Manejo de números negativos
    numero = abs(numero)
    
    # Inicializar el contador de bits en 0
    bits = 0
    
    # Caso especial para el número 0
    if numero == 0:
        return 1

    # Calcular la cantidad de bits necesarios
    while numero > 0:
        bits += 1
        numero //= 2

    return bits


# Función para generar la tabla de codificación
def tabla_de_codificacion(texto, longitud_binarios):
    bigramas = contar_bigramas(texto)

    # Filtrar bigramas con más de una aparición y contar letras individuales
    bigramas_filtrados = {bigrama: frecuencia for bigrama, frecuencia in bigramas.items() if frecuencia > 10}
    letras_individuales = {}
    for letra in texto:
        if letra not in letras_individuales:
            letras_individuales[letra] = texto.count(letra)

    # Ordenar los resultados por frecuencia de mayor a menor
    bigramas_ordenados = dict(sorted(bigramas_filtrados.items(), key=lambda item: item[1], reverse=True))
    letras_ordenadas = dict(sorted(letras_individuales.items()))

    tabla_codificacion = {}
    posicion = 0

    total_elementos_tabla_codificsacion = len(bigramas_ordenados) + len(letras_ordenadas) 
    longitud_binarios =  contar_bits_necesarios(total_elementos_tabla_codificsacion)

    for bigrama, _ in bigramas_ordenados.items():
        binario = format(posicion, '0' + str(longitud_binarios) + 'b')
        tabla_codificacion[bigrama] = binario
        posicion += 1

    for letra, _ in letras_ordenadas.items():
        binario = format(posicion, '0' + str(longitud_binarios) + 'b')
        tabla_codificacion[letra] = binario
        posicion += 1

    return tabla_codificacion

# Función para codificar el texto
def texto_codificado(texto, tabla_codificacion):
    codigo = ""
    i = 0
    while i < len(texto):
        bigrama = texto[i:i+2]

        if bigrama in tabla_codificacion:
            codigo += tabla_codificacion[bigrama]
            i += 2
        else:
            letra = texto[i]
            codigo += tabla_codificacion[letra]
            i += 1

    return codigo

# Función para decodificar el código
def decodificar_codigo(codigo_texto, tabla_codificacion):
    texto_decodificado = ""
    longitud_binarios = len(list(tabla_codificacion.values())[0])
    i = 0
    while i < len(codigo_texto):
        encontrado = False
        for simbolo, binario in tabla_codificacion.items():
            binario_codigo = codigo_texto[i:i+longitud_binarios]
            if codigo_texto[i:i+longitud_binarios] == binario:
                texto_decodificado += simbolo
                i += longitud_binarios
                encontrado = True
                break
        if not encontrado:
            return "Error: No se pudo decodificar el código."

    return texto_decodificado

def Punto_2_diagrama():
    texto_original = leer_archivo()
    bits = int(input("Ingrese la longitud de los binarios: "))

    tabla_codificacion = tabla_de_codificacion(texto_original, bits)
    codigo = texto_codificado(texto_original, tabla_codificacion)
    texto_decodificado = decodificar_codigo(codigo, tabla_codificacion)

    print("Texto original:")
    print(texto_original)
    print("\nTabla de Codificación:")
    for simbolo, binario in tabla_codificacion.items():
        print(f"{simbolo}:\t{binario}")
    print("\nTexto codificado:")
    print(codigo)
    print("\nTexto decodificado:")
    print(texto_decodificado)

    longitud_texto = len(texto_original)
    print("longitud:",longitud_texto)

    #para modificar el largo (numero de digitos) codigo binario modificar linea 177 modificar ># (10)  
    # bigramas_filtrados = {bigrama: frecuencia for bigrama, frecuencia in bigramas.items() if frecuencia > 10}

    # total bits bigrama = largo (numero de digitos) codigo binario * cantidad de bigramas de tabla de codificacion 
    total_bits_bigrama = (len(texto_original)/2)*bits
    print("total bits bigrama: ",total_bits_bigrama) # 222 

    # total_bits_longitud_fija = logaritmo en base 2 (caracteres individuales)* largo (numero de digitos) codigo binario
    cantidad_caracteres_texto = contar_caracteres_individuales 
    cantidad_caracteres = len (cantidad_caracteres_texto)
    total_bits_longitud_fija = math.log(cantidad_caracteres,2)*longitud_texto
    print ("total bits longitud fija: ", total_bits_longitud_fija)  

    #Rata de compresion = total_bits_longitud_fija/total_bits_bigrama
    print("Rc:",total_bits_longitud_fija/total_bits_bigrama)

#------------------------------------------------------------------------------------------------------------------------------
# menu
num =5
while num != 0:

    print("Tarea 2: teoria de la informacion \n \n ")
    print("Selecciones una opcion \n ")
    print ("1. Codificacion Huffman.")
    print ("2. Codificacion Diagrama.")
    print ("3. Codificacion LZ78.")
    print ("4. Codificacion LZW.")
    print ("0. Salir.")

    num = int(input("Ingrese el número de la opción deseada: "))
  
    if num == 1:   
        punto_1_huffman()
    elif num == 2: 
        Punto_2_diagrama()  
    elif num == 3: 
        print ("Codificacion LZ78.")
    elif num == 4: 
        print ("Codificacion LZW.")




