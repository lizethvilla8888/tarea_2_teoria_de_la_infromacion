
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

# Función para generar la tabla de codificación
def tabla_de_codificacion(texto, bits):
    bigramas = contar_bigramas(texto)

    # Filtrar bigramas con más de una aparición y contar letras individuales
    bigramas_filtrados = {bigrama: frecuencia for bigrama, frecuencia in bigramas.items() if frecuencia > 1}
    letras_individuales = {}
    for letra in texto:
        if letra not in letras_individuales:
            letras_individuales[letra] = texto.count(letra)

    # Ordenar los resultados por frecuencia de mayor a menor
    bigramas_ordenados = dict(sorted(bigramas_filtrados.items(), key=lambda item: item[1], reverse=True))
    cantidad_bigramas = len(bigramas_ordenados)
    letras_ordenadas = dict(sorted(letras_individuales.items()))

    letras_individuales = len(letras_ordenadas)
    tabla_codificacion = {}
    posicion = 0

    for bigrama, _ in bigramas_ordenados.items():
        binario = format(posicion, '0' + str(bits) + 'b')
        tabla_codificacion[bigrama] = binario
        posicion += 1

    for letra, _ in letras_ordenadas.items():
        binario = format(posicion, '0' + str(bits) + 'b')
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
            if codigo_texto[i:i+longitud_binarios] == binario:
                texto_decodificado += simbolo
                i += longitud_binarios
                encontrado = True
                break
        if not encontrado:
            return "Error: No se pudo decodificar el código."

    return texto_decodificado



# Resto del código
texto_original = "a_cuesta_le_cuesta_subir_la_cuesta_y_en_medio_de_la_cuesta_va_y_se_acuesta"
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

print("longitud:", len(texto_original))
total_bits_bigrama = (len(texto_original)/2)*bits
print("total bits bigrama: ",(len(texto_original)/2)*bits) # 222 

total_bits_longitud_fija= len(texto_original)*bits
print("total bits longitud fija: ", len(texto_original)*bits)#370
print("Rc:",total_bits_longitud_fija/total_bits_bigrama)







