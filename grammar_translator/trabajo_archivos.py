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
    
  lista_de_reglas = [] 
  no_encontradas =  []                  
  for no_terminal, banco_de_reglas in banco_de_reglas.items():
    if no_terminal in lista_no_terminales:
      regla_separada = " | ".join(banco_de_reglas)
      regla_formateada ="{} -> {}".format(no_terminal,regla_separada) 
      lista_de_reglas.append(regla_formateada)
  return lista_de_reglas




    












