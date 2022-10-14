import json
import re

#Función que abre el txt con la gramatica categorial. Recibe el nombre del archivo por parametro y devuelve un string con la gramática
def abrir_gramatica_categorial(nombre_archivo):
    path = f"gramaticas/{nombre_archivo}.txt"
    with open(path,'r', encoding="utf-8") as archivo:
        gramatica = archivo.read()
    return gramatica

#Función que devuelve el diccionario de reglas que corresponda según el idioma y la gramática.

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

def creacion_gramatica(simbolos, banco_de_reglas):
    '''
        Funcion que busca para armar una gramàtica. Trae
        todas las reglas donde estèn incluìdos los sìmbolos
        pasados por paràmetro, luego busca todas las reglas 
        para los sìmbolos que aparecieron en la bùsqueda
        anterior y asì sucesivamente hasta llegar a las reglas 
        màs abstractas.

        Parametros
        ----------
        simbolos: list
            Lista de las categorìas de los sìmbolos no 
            terminales de una gramàtica.

        banco_de_reglas: dict
            Diccionario que contiene reglas de una gramàtica
            donde las keys son los sìmbolos no terminales y
            los values son listas con las reglas de reescritura
            posibles de dicho sìmbolo:
                {"SV": ["V", "V SN"]}
            
        Returns
        -------
        list
            Lista con las reglas formateadas.
    '''
  simbolos_copia = simbolos
  go = True
  while go == True:
    reglas, simbolos_nt = buscador_de_reglas(simbolos_copia, banco_de_reglas)
    simbolos_nuevos = [s for s in simbolos_nt if s not in simbolos_copia]
    if simbolos_nuevos:
      simbolos_copia = simbolos_copia + simbolos_nuevos
    else: 
      go = False
  return list(set(reglas))

def buscador_de_reglas(simbolos, banco_de_reglas):
    '''
        Funcion que busca reglas para sìmbolos no terminales.

        Parametros
        ----------
        simbolos: list
            Lista de sìmbolos no terminales.

        banco_de_reglas: dict
            Diccionario que contiene reglas de una gramàtica
            donde las keys son los sìmbolos no terminales y
            los values son listas con las reglas de reescritura
            posibles de dicho sìmbolo:
                {"SV": ["V", "V SN"]}
            
        Returns
        -------
        tuple
            lista_de_reglas: list
                Lista con las reglas que contienen alguno de los
                sìmbolos no terminales pasados por paràmetro.

            list
                Lista de las keys de las cuales se extrajeron las
                reglas de lista_de_reglas.
    '''
    lista_de_reglas = []
    lista_de_keys = []
    for key, value in banco_de_reglas.items():
      for simbolo in simbolos:
        regexp = re.compile(r'\b{}\b'.format(simbolo)) 
        for v in value:
          if regexp.search(v):
            regla_formateada ="{} -> {}".format(key,v) 
            lista_de_reglas.append(regla_formateada)
            lista_de_keys.append(key) 
    return lista_de_reglas, list(set(lista_de_keys))

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