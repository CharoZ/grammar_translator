import json


#Función que abre el txt con la gramatica categorial. Recibe el nombre del archivo por parametro y devuelve un string con la gramática
def abrir_gramatica_categorial(nombre_archivo):
    path="gramaticas/" + nombre_archivo + ".txt"
    with open(path,'r', encoding="utf-8") as archivo:
        gramatica = archivo.read()

    return gramatica

#Función que abre el diccionario de reglas que corresponda según el idioma y la gramática. Devuelve el diccionario de reglas
def cargar_diccionario_reglas(idioma, gramatica):
    if(idioma =='es'and gramatica =='cfg'):
        with open('../data/cfg.json', 'r') as archivo:
            diccionario = json.load(archivo)
    
    return diccionario

#Funcion que recibe una gramatica en forma de lista, la convierte en un string separado por /n 
#Guarda la gramática resultante en un archivo (CFG)s
def guardar_cfg_final(gram_completa):
    resultado = "\n".join(gram_completa)
    with open('gramaticas/resultado.cfg','w+') as out:
        out.write(resultado)
    return None



#Prueba de las funciones

gram_categorial = abrir_gramatica_categorial("output")
print(gram_categorial)

# guardarla en una lista separada por lineas
lista_cfg_final = gram_categorial.split("\n")

print(lista_cfg_final)

diccionario = cargar_diccionario_reglas(idioma='es',gramatica='cfg')
print(diccionario)


guardar_cfg_final(lista_cfg_final)




    












