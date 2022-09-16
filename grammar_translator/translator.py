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

def buscador_de_reglas(banco_de_reglas,lista_no_terminales):
    '''
    Función que busca reglas para una lista de símbolos no terminales.
    Devuelve una lista con las reglas encontradas 

    Parámetros
    ----------
    banco_de_reglas: dic
        Diccionario con las reglas de una gramática

    lista_de_no_terminales: list
        Lista de símbolos no terminales extraídos de la gramática ingresada
        por el usuario

    Returns
    -------
    lista_de_reglas: list
        Lista que contiene los símbolos no terminales con las reglas de 
        reescritura que corresponden a cada uno. 

    '''
    lista_de_reglas = []
    for no_terminal in lista_no_terminales:
        if no_terminal in banco_de_reglas.keys():
            regla = banco_de_reglas[no_terminal]
            regla_separada = " | ".join(regla)
            regla_formateada ="{} -> {}".format(no_terminal,regla_separada) 
            lista_de_reglas.append(regla_formateada)
        else:
            no_terminal not in banco_de_reglas.keys():
            print(f'\n\033[1;33m**Atención** No se encontraron reglas para {no_terminal}\033[0;0m\n')  
    return lista_de_reglas






    












