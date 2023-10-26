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

def calculo_de_probabilidad_simbolos(texto, tabla_codificacion):
    probabilidad_simbolos = {}
    total_simbolos = len(texto)
    print ("texto que esta resiviendo caluclo de probabiidad: \n \n \n  ")
    print(texto)
    for simbolo, codigo in tabla_codificacion.items():
        frecuencia = texto.count(simbolo)
        probabilidad = frecuencia / total_simbolos
        probabilidad_simbolos[simbolo] = probabilidad

    return probabilidad_simbolos

def Informacion_cd_simbolo(probabilidad_simbolos):
    informacion_simbolos = {}
    
    for simbolo, probabilidad in probabilidad_simbolos.items():
        informacion = math.log2(1 / probabilidad)
        informacion_simbolos[simbolo] = informacion
    
    return informacion_simbolos

def entropia_cd_simbolo(informacion_simbolos, probabilidad_cd_simbolo):
    entropias_por_simbolo = {}
    suma_entropias = 0.0
    
    for simbolo in informacion_simbolos:
        entropia = informacion_simbolos[simbolo] * probabilidad_cd_simbolo[simbolo]
        entropias_por_simbolo[simbolo] = entropia
        suma_entropias += entropia
    
    return suma_entropias

def longitud_promedio_cd_codigo(tabla_codificacion, probabilidad_simbolos):
    sumas_por_simbolo = {}
    suma_longitudes = 0.0
    
    for simbolo, codigo in tabla_codificacion.items():
        probabilidad = probabilidad_simbolos.get(simbolo, 0)  # Obtiene la probabilidad del símbolo o 0 si no se encuentra
        longitud = len(codigo)
        pxl = probabilidad * longitud
        sumas_por_simbolo[simbolo] = pxl
        suma_longitudes += pxl
    
    return  suma_longitudes

def punto_1_huffman():
    print("Codificacion Huffman ") 
    if __name__ == '__main__':
       #texto = leer_archivo()
       texto = "aaaaaaaeii"

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

    # Llama a la función con el texto y la tabla de codificación
    tabla_codificacion = construir_tabla_codificacion(arbol_huffman)
    probabilidades = calculo_de_probabilidad_simbolos(texto_original, tabla_codificacion)
    informacion_simbolos = Informacion_cd_simbolo(probabilidades)
    entropia = entropia_cd_simbolo(informacion_simbolos,probabilidades)
    longitud_promedio = longitud_promedio_cd_codigo(tabla_codificacion, probabilidades)
    eficiencia =  entropia / longitud_promedio
    redundancia = 1 - eficiencia
    tasa_compresion = (len(texto)*8)/(len(texto_codificado))
    
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
def tabla_de_codificacion(texto):
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

    tabla_codificacion = tabla_de_codificacion(texto_original)
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

    probabilidades = calculo_de_probabilidad_simbolos(texto_original, tabla_codificacion)
    informacion_simbolos = Informacion_cd_simbolo(probabilidades)
    entropia = entropia_cd_simbolo(informacion_simbolos,probabilidades)
    longitud_promedio = longitud_promedio_cd_codigo(tabla_codificacion, probabilidades)
    eficiencia =  entropia / longitud_promedio
    redundancia = 1 - eficiencia
    tasa_compresion = (len(texto_original)*8)/(len(codigo))
    
    print("Eficiencia:", eficiencia)
    print("Redundancia:", redundancia)
    print("Tasa de compresión:", tasa_compresion, "%","\n \n ")


#------------------------------------------------------------------------------------------------------------------------------
# LZ78 
def codificar_LZ78(texto):
    diccionario = {}
    resultado = []
    buffer = ''
    indice = 0

    while indice < len(texto):
        simbolo = texto[indice]
        if buffer + simbolo in diccionario:
            buffer += simbolo
        else:
            if buffer:
                resultado.append((diccionario[buffer], simbolo))
            else:
                resultado.append(("", simbolo))
            diccionario[buffer + simbolo] = len(diccionario) + 1
            buffer = ''
        indice += 1

    codificacion_binaria = []

    for (indice, simbolo) in resultado:
        if indice == "":
            binario = "0"
        else:
            binario = format(indice, 'b')
        codificacion_binaria.append((binario, simbolo))

    return codificacion_binaria, resultado
def decodificar_LZ78(codificacion):
    diccionario = {0: ''}
    texto = ''
    for (indice, simbolo) in codificacion:
        if indice == "":
            cadena = simbolo
        else:
            cadena = diccionario[int(indice, 2)] + simbolo
        diccionario[len(diccionario)] = cadena
        texto += cadena
    return texto

def punto_3_LZ78():
    texto_original = leer_archivo()
    codificacion_binaria, resultado = codificar_LZ78(texto_original)
    texto_descodificaco = decodificar_LZ78(codificacion_binaria)
    # Calcular la longitud promedio de la codificación
    LongitudPromedio = sum(len(indice) for indice, _ in codificacion_binaria) / len(codificacion_binaria)

    # Calcular la entropía
    Letras = set(texto_original)
    Entropia = -sum((texto_original.count(letra) / len(texto_original)) * math.log2(texto_original.count(letra) / len(texto_original) + 1e-10) for letra in Letras)

    # Calcular la eficiencia y redundancia
    Eficiencia = Entropia / LongitudPromedio
    Redundancia = 1 - Eficiencia


    # Calcular la tasa de compresión
    BitsOriginales = len(texto_original) * 8  # Multiplicado por 8 para convertir a bits
    BitsCompresion = sum(len(indice) + 8 for indice, _ in codificacion_binaria)  # Sumar 8 bits por cada símbolo
    Rata = BitsOriginales / BitsCompresion

    print("Texto original:", texto_original)
    #print(codificacion_binaria)
    texto_comprimido = ''.join([indice for indice, _ in codificacion_binaria])
    print("Codificación LZ78 (en binario):", texto_comprimido)
    print("Descodificacion del texto:", texto_descodificaco)
    print("Eficiencia =", Eficiencia)
    print("Redundancia =", Redundancia)
    print("Rata de compresión =", Rata)

#-----------------------------------------------------------------------------------------------------------------------------
#lZW
DiccionarioLZW = {}


def ConvertirABinarioBase(Numero, BitsMaximos):
    Binario=bin(int(Numero))
    Binario=Binario[2:]
    Binario="0"*(BitsMaximos-len(Binario))+Binario
    return Binario

def LetrasUnicas(texto):
    Contador = 0
    for letra in texto:
        if letra not in DiccionarioLZW.keys():
            DiccionarioLZW[letra] = Contador
            Contador += 1

def CodificacionLZW(Texto):
    global DiccionarioLZW
    LetrasUnicas(Texto)
    temp=0
    Salida=""
    for PosicionLetra in range(len(Texto)-1):
        Extra=2
        if PosicionLetra+temp+Extra>len(Texto):
            break

        Concatenacion=Texto[PosicionLetra+temp:PosicionLetra+temp+Extra]
        if Concatenacion in DiccionarioLZW.keys():
            Conversion=str(DiccionarioLZW[Concatenacion])
            Salida=Salida+ Conversion+":"
        else:
            SinUltimo=Concatenacion[:len(Concatenacion)-1]
            Conversion=str(DiccionarioLZW[SinUltimo])
            Salida=Salida+Conversion+":"
        while Texto[PosicionLetra+temp:PosicionLetra+temp+Extra] in DiccionarioLZW.keys():
            Extra+=1
            if PosicionLetra+temp+Extra>=len(Texto):
                break
        if Concatenacion not in DiccionarioLZW.keys():
            DiccionarioLZW[Texto[PosicionLetra+temp:PosicionLetra+temp+Extra]]=len(DiccionarioLZW)
        temp+=Extra-2
    
    SalidaReal=""
    Numero=len(DiccionarioLZW)
    Salida=Salida[:len(Salida)-1]
    ListaCodigo=Salida.split(":")
    BitsMaximos=math.ceil(math.log2(Numero))

    for Numero in ListaCodigo:
        SalidaReal=SalidaReal+ConvertirABinarioBase(Numero, BitsMaximos)
    MaximoEnBinario=bin(BitsMaximos)
    MaximoEnBinario=MaximoEnBinario[2:]
    MaximoEnBinario="0"*(4-len(MaximoEnBinario))+MaximoEnBinario
    SalidaReal= MaximoEnBinario+SalidaReal
    DiccionarioLZW={Valor: Llave for (Llave, Valor) in DiccionarioLZW.items()}
    return SalidaReal

def DecodificadorLZW(Codigo, DiccionarioLZW):
    Particion=int(Codigo[:4],2)
    ListaDeCodigos=[]
    Texto=""
    Codigo1=Codigo[4:]
    while len(Codigo1)!=0:
        ListaDeCodigos.append(Codigo1[:Particion])
        Texto=Texto+DiccionarioLZW[int(Codigo1[:Particion],2)]
        Codigo1=Codigo1[Particion:]
    print(Texto)

def DatosLZW(Diccionario, Texto, Codigo):
    LongitudPromedio=int(Codigo[:4],2)
    
    #Calculo Entropia

    Letras=[]
    for Llave in Diccionario.keys():
        if [Diccionario[Llave],Texto.count(Diccionario[Llave])] not in Letras:
            if len(Diccionario[Llave])!=1:
                Letras.append([Diccionario[Llave],Texto.count(Diccionario[Llave])])
    Entropia=0
    Tam=len(Texto)
    for Par in Letras:
        Probabilidad=(Par[1]/Tam)
        Entropia+=Probabilidad*math.log2(1/Probabilidad)
    Eficiencia=Entropia/LongitudPromedio
    Redundancia=1-Eficiencia
    Total=Eficiencia+Redundancia

    #Ratio
    BitsOriginales=Tam*8
    BitsCompresion=len(Codigo)
    Rata=BitsOriginales/BitsCompresion
    print("La eficiencia de la compresión LZW fue de ", Eficiencia)
    print("La redundancia por tanto fue de ", Redundancia)
    print("La rata de compresión fue de ", Rata)


#-------------------------------------------------------------------------------------------------------------------------------
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
        print ("Codificacion Huffman.\n")
        punto_1_huffman()
    elif num == 2: 
        print ("Codificacion Digrama.\n")
        Punto_2_diagrama()  
    elif num == 3: 
        print ("Codificacion LZ78.\n")
        punto_3_LZ78()
    elif num == 4: 
        print ("Codificacion LZW.\n")
        Texto2 = leer_archivo()
        CodigoLZW = CodificacionLZW(Texto2[:])
        DatosLZW(DiccionarioLZW,Texto2, CodigoLZW)





