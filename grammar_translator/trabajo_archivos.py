import json


#Función que abre el txt con la gramatica categorial. Recibe el nombre del archivo por parametro y devuelve un string con la gramática
def abrir_gramatica_categorial(nombre_archivo):
    path = f"gramaticas/{nombre_archivo}.txt"
    with open(path,'r', encoding="utf-8") as archivo:
        gramatica = archivo.read()

    return gramatica

#Función que devuelve el diccionario de reglas que corresponda según el idioma y la gramática.
import json

def cargar_diccionario_reglas(idioma, gramatica):
    
    path = f"../data/{gramatica}.json"
    with open(path, 'r') as file:
        diccionarios = json.load(file)
     
    banco_reglas=diccionarios[idioma]
            
    return banco_reglas

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




    












