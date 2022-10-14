import json
import re
import spacy

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

def primer_buscador(simbolos, banco_de_reglas):
  simbolos_copia = simbolos
  go = True
  while go == True:
    reglas, simbolos_nt = segundo_buscador(simbolos_copia, banco_de_reglas)
    simbolos_nuevos = [s for s in simbolos_nt if s not in simbolos_copia]
    if simbolos_nuevos:
      simbolos_copia = simbolos_copia + simbolos_nuevos
    else: 
      go = False
  return list(set(reglas))

def segundo_buscador(simbolos, banco_de_reglas):
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

        Parámetros
        ----------
        gramatica_categorial: str
            Gramática para preprocesar.
            
        Returns
        -------
        lista_terminales: list
            Lista con los símbolos terminales de la gramática.
    '''
    lineas = gramatica_categorial.split('\n')
    lista_terminales = []
    for l in lineas:
        primer_simbolo = l.split(' =>')[0]
        sin_blancos = re.sub(r'\s', '', primer_simbolo)
        if sin_blancos and not sin_blancos.isupper():
            lista_terminales.append(sin_blancos)
    return lista_terminales

def busqueda_de_categoria(terminal):
    '''
        Función que realiza la equivalencia de categorias que usa
        spacy y las que se usan en la cfg.

        Parámetros
        ----------
        terminal: spacy.tokens.token.Token
            Palabra analizada por el modelo de spacy.
            
        Returns
        -------
        simbolo: str
            String con la categoría que le corresponde a la palabra. 
    '''
    simbolo = None
    if terminal.pos_ == "NOUN":
        simbolo = "NC"
    elif terminal.pos_ == "PROPN":
        simbolo = "NP"
    elif terminal.pos_ == "VERB":
        morph = list(terminal.morph)[-1]
        if morph.endswith("Part"):
            simbolo = "PART"
        else:
            simbolo = "V"
    elif terminal.pos_ == "DET":
        simbolo = "D"
    elif terminal.pos_ == "PRON":
        simbolo = "PRO"
    elif terminal.pos_ == "AUX":
        simbolo = "AUX"
    elif terminal.pos_ == "ADP":
        simbolo = "P"
    elif terminal.pos_ == "SCONJ":
        simbolo = "PROREL"
    elif terminal.pos_ == "CCONJ":
        simbolo = "CONJ"
    elif terminal.pos_ == "ADJ":
        simbolo = "ADJ"
    elif terminal.pos_ == "ADV":
        simbolo = "ADV"   
    return simbolo
 
def traduccion_terminales(lista_terminales):
    '''
        Función que recibe la lista de terminales y 
        devuelve un diccionario de terminales con su 
        categoría y una lista de no terminales. Si no
        encuentra categoría para una palabra se imprime
        una advertencia por consola.

        Parámetros
        ----------
        lista_terminales: list
            Lista compuesta de strings con los símbolos
            terminales de la gramática.
            
        Returns
        -------
        tuple
            diccionario_terminales: dict
                Contiene los símbolos terminales como 
                keys y sus respectivas categorías como values.

            no_terminales: list 
                Lista con todas las categorías obtenidas 
                en el diccionario.
    '''
    nlp = spacy.load("es_core_news_sm")
    terminales_string = ' '.join(lista_terminales)
    doc = nlp(terminales_string)
    diccionario_terminales = {}
    for token in doc:
        simbolo=busqueda_de_categoria(token)
        if simbolo:
            diccionario_terminales[token.text]=simbolo
        else:
            print(f"\033[1;33mNo se encontró categoría para \"{token}\", se debe agregar manualmente.\033[0;0m")
    no_terminales = list(set(diccionario_terminales.values()))
    return diccionario_terminales, no_terminales

def traduccion_gramatica(nombre_archivo, idioma, gramatica):
    '''
        Función que traduce una gramática categorial, la 
        traduce y luego la guarda como una cfg.

        Parámetros
        ----------
        nombre_archivo: str
            Nombre del archivo que contiene la gramática
            a traducir.

        idioma: str
            Código del idioma en el que se está 
            trabajando.

        gramatica: str
            Tipo de gramática a la que se quiere traducir,
            hoy solo es cfg.
            
        Returns
        -------
        reglas_completas: str
            Gramática traducida. 
    '''
    print("Cargando archivos")
    categorial = abrir_gramatica_categorial(nombre_archivo)
    banco_reglas = cargar_diccionario_reglas(idioma, gramatica)
    print("Iniciando traducción")
    lista_terminales = preprocesamiento(categorial)
    terminales_taggeados, no_terminales = traduccion_terminales(lista_terminales)
    reglas_nt = primer_buscador(no_terminales, banco_reglas) #nombre de fn
    reglas_completas = funcion_check_final_por_hacer(reglas_nt, terminales_taggeados)
    print("Guardando resultados")
    guardar_cfg_final(reglas_completas) #un parametro mas
    return reglas_completas