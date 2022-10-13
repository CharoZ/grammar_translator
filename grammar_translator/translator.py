import json
import re

def abrir_gramatica_categorial(nombre_archivo):
    '''
        Funcion que abre y lee un archivo que contiene gramatica categorial. Devuelve la gramatica
        Parametros
        ----------
        nombre_archivo: str
            nombre del archivo que contiene la gramatica.
            
        Returns
        -------
        gramatica: str
            Gramatica categorial
    '''
    path = f"gramaticas/{nombre_archivo}.txt"
    with open(path,'r', encoding="utf-8") as archivo:
        gramatica = archivo.read()
    return gramatica


def cargar_diccionario_reglas(idioma, gramatica):
    '''
        Funcion que abre y lee un archivo que contiene un diccionario de reglas. Devuelve
        las reglas segun la gramatica y el idioma pasados por parametros.
        Parametros
        ----------
        idioma: str
            idioma del diccionario.
        gramatica: str
            nombre del archivo.
            
        Returns
        -------
        banco_reglas: dict
            Diccionario con las reglas de la gramatica
    '''
    path = f"../data/{gramatica}.json"
    with open(path, 'r') as file:
        diccionarios = json.load(file)
    banco_reglas=diccionarios[idioma] 
    return banco_reglas


def guardar_cfg_final(gram_completa):
    '''
        Funcion que formatea y guarda una gramatica en un archivo "resultado.cfg" dentro del directorio "gramaticas". 
        Parametros
        ----------
        gram_completa: List
            Gramatica para procesar.
            
        Returns
        -------
        None
    '''
    resultado = "\n".join(gram_completa)
    with open('gramaticas/resultado.cfg','w+') as out:
        out.write(resultado)
    return None


def preprocesamiento(gramatica_categorial):
    '''
        Funcion que preprocesa la gramatica categorial. Devuelve
        simbolos terminales.
        Parametros
        ----------
        gramtica_categorial: str
            Gramatica para preprocesar.
            
        Returns
        -------
        lista_terminales: list
            Lista con los simbolos terminales de la gramatica.
    '''
    lineas = gramatica_categorial.split('\n')
    lista_terminales = []
    for l in lineas:
        primer_simbolo = l.split(' =>')[0]
        sin_blancos = re.sub(r'\s', '', primer_simbolo)
        if sin_blancos and not sin_blancos.isupper():
            lista_terminales.append(sin_blancos)
    return lista_terminales