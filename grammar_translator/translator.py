import json
import re
import spacy

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


def guardar_cfg_final(gram_completa, nombre_archivo):
    '''
        Funcion que formatea y guarda una gramatica en un archivo "resultado.cfg" dentro del directorio "gramaticas". 
        Parametros
        ----------

        gram_completa: List
            Gramatica para procesar.

        nombre_archivo: str
            nombre del archivo que contiene la gramatica.
            
        Returns
        -------
        None
    '''
    resultado = "\n".join(gram_completa)
    with open(f'gramaticas/{nombre_archivo}_cfg.cfg','w+') as out:
        out.write(resultado)
    return None

def creacion_gramatica(simbolos, banco_de_reglas):
    '''
        Funcion que busca para armar una gramàtica. Trae
        todas las reglas donde estèn incluìdos los sìmbolos
        pasados por paràmetro, luego busca todas las reglas 
        para los sìmbolos que aparecieron en la búsqueda
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
    diccionario_terminales = {}
    for palabra in lista_terminales:
        palabra = nlp(palabra)
        token=palabra[0]
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
    reglas_nt = creacion_gramatica(no_terminales, banco_reglas)
    reglas_completas = unificacion_y_chequeo_reglas(reglas_nt, terminales_taggeados)
    print("Guardando resultados")
    guardar_cfg_final(reglas_completas, nombre_archivo)
    return reglas_completas