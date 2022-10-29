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
    path = f"data/{gramatica}.json"
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
        path_gramatica : str
            path completo al archivo resultante
    '''
    resultado = "\n".join(gram_completa)
    path_gramatica = f'gramaticas/{nombre_archivo}_cfg.cfg'
    with open(path_gramatica,'w+') as out:
        out.write(resultado)
    return path_gramatica

def creacion_gramatica(simbolos, banco_de_reglas):
    '''
        Funcion que busca para armar una gramática. Trae
        todas las reglas donde estén incluídos los símbolos
        pasados por parámetro, luego busca todas las reglas 
        para los símbolos que aparecieron en la búsqueda
        anterior y así sucesivamente hasta llegar a las reglas 
        más abstractas.

        Parametros
        ----------
        simbolos: list
            Lista de las categorías de los símbolos no 
            terminales de una gramática.

        banco_de_reglas: dict
            Diccionario que contiene reglas de una gramática
            donde las keys son los símbolos no terminales y
            los values son listas con las reglas de reescritura
            posibles de dicho símbolo:
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
        Funcion que busca reglas para símbolos no terminales.

        Parametros
        ----------
        simbolos: list
            Lista de símbolos no terminales.

        banco_de_reglas: dict
            Diccionario que contiene reglas de una gramática
            donde las keys son los símbolos no terminales y
            los values son listas con las reglas de reescritura
            posibles de dicho símbolo:
                {"SV": ["V", "V SN"]}
            
        Returns
        -------
        tuple
            lista_de_reglas: list
                Lista con las reglas que contienen alguno de los
                símbolos no terminales pasados por parámetro.

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
        palabra_procesada = nlp(palabra)
        token=palabra_procesada[0]
        simbolo=busqueda_de_categoria(token)
        if simbolo:
            diccionario_terminales[token.text]=simbolo
        else:
            print(f"\033[1;33mNo se encontró categoría para \"{token}\", se debe agregar manualmente.\033[0;0m")
    no_terminales = list(set(diccionario_terminales.values()))
    return diccionario_terminales, no_terminales

def unificacion_de_reglas(reglas_nt, terminales_taggeados):
    '''
        Función que recibe una lista de reglas de reescritura y 
        un diccionario de terminales con su categoría, y devuelve
        reglas para todos los símbolos con un mismo formato.

        Parámetros
        ----------
        reglas_nt: list
            Lista compuesta de strings con las reglas para los símbolos 
            no terminales.

        terminales_taggeados: dict
            Diccionario que contiene todos los símbolos terminales como
            keys y sus respectivas categorías como values.
            
        Returns
        -------
        reglas_totales: list 
            Lista con todas las reglas necesarias para la gramática en orden.
    '''
    reglas_nt_sin_inicial = []
    inicial = []
    for regla in reglas_nt:
        if regla.startswith("S ->"):
            inicial.append(regla)
        else:
            reglas_nt_sin_inicial.append(regla)
    lista_taggeados = []
    nuevo_dict = {}
    for k, v in terminales_taggeados.items():
        if v not in nuevo_dict.keys():
            nuevo_dict[v] = [k]
        else:
            nuevo_dict[v].append(k)
    for k, v in nuevo_dict.items():
        lista_taggeados.append('{} -> \'{}\''.format(k, '\' | \''.join(v)))
    reglas_totales = inicial + reglas_nt_sin_inicial + lista_taggeados
    return reglas_totales
    
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
    reglas_completas = unificacion_de_reglas(reglas_nt, terminales_taggeados)
    print("Guardando resultados")
    cfg_resultante = guardar_cfg_final(reglas_completas, nombre_archivo)
    print(f'El archivo se guardó en {cfg_resultante}')
    return reglas_completas