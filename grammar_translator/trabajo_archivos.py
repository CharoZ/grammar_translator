#Abrir y leer gramática
#pedir el nombre del archivo y reemplazar 
# ver pasarle un parametro para lo de los acentos
#levantar categorial
def funcion_que_levanta_gram_categorial(nombre_archivo):
    path="gramaticas/" + nombre_archivo + ".txt"
    with open(path) as archivo:
        gramatica = archivo.read()

    return gramatica
    
gram_categorial = funcion_que_levanta_gram_categorial("output")
print(gram_categorial)

# guardarla en una lista separada por lineas
list = gram_categorial.split("\n")
print(list)


#Funcion que recibe una gramatica en forma de lista, la convierte en un string separado por /n 
#Guarda la gramática resultante en un archivo (CFG)s
def funcion_que_guarda_cfg_final(gram_completa):
    result = "\n".join(gram_completa)
    with open('gramaticas/resultado.cfg','w+') as out:
        out.write(result)
    return None

funcion_que_guarda_cfg_final(list)