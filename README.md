# grammar_translator

## 1. Instalación

### 1.1. Python y pip

Para poder utilizar el repositorio con el entorno que le corresponde es necesario tener instalada alguna versión de python 3.8 en la computadora. A su vez es necesario contar con pip instalado. En caso de no tenerlo, se debe instalar de la siguiente forma: 

```
sudo apt install python3-pip
```

### 1.2. Instalación pipenv

Para acceder al entorno que fue creado para el repositorio se debe instalar la librería pipenv
```
pip3 install pipenv
```

### 1.3. Creación del entorno

Una vez que todo esté instalado, hay que moverse al directorio raíz del repositorio y correr el siguiente comando:

```
pipenv install
```

Esto creará el entorno con todas las dependencias necesarias para poder usar el código. Dentro de este entorno se encuentra instalado este repositorio como un paquete, es decir, puede importarse del siguiente modo:

```
import grammar_translator as gt
```

Este último comando sirve si se quieren importar las funciones que forman parte del código de este repositorio. 

#### 1.3.1 Entorno para demo y contribuciones

Si se quiere utilizar la demo incluida en el repositorio, el entorno deberá instalarse con el siguiente comando: 

```
pipenv install --dev
```

Esta instalación incluye pytest y jupyterlab, por lo cual también puede ser útil si se quiere hacer una colaboración de código, o si por alguna razón el usuario quisiera crear notebooks propias dentro del repositorio. 

## 2. Utilización del traductor

Si se quiere utilizar para traducción de gramaticas se deben seguir ciertos pasos:

#### 2.1. Carga de gramática

Se debe dejar el archivo .txt que contiene una gramática categorial dentro de la carpeta _gramaticas/_. Se recomienda que el nombre del archivo no contenga espacios en blanco.

El script necesitará que todos los símbolos no terminales estén escritos en mayúscula, y que los terminales sólo contengan, de ser necesario, una mayúscula inicial, pero continúen en minúscula (Por ejemplo, en el caso de entidades como la Universidad de Buenos Aires, en lugar de llamarla "UBA" se la deberá llamar "Uba").

#### 2.2. Traducción

Una vez que se tiene la gramática en la carpeta correspondiente se debe abrir la consola y correr el siguiente comando desde el directorio raíz del repositorio:

```
pipenv run python traductor_gramatica.py ＜nombre_del archivo_a_traducir＞
```

Es importante no incluir la extensión del archivo (.txt), ya que el código lo reconoce automáticamente.
El idioma por default será español por ser el único disponible por el momento. La traducción será a una gramatica cfg por ser la única disponible en el momento. 

#### 2.3. Resultados

Una vez terminado el paso anterior la gramática traducida estará guardada en _gramaticas/＜nombre_del archivo_a_traducir＞_cfg.cfg_. Tendrá el mismo nombre que el archivo de input pero con distinta extensión. 

WARNING: Es posible que durante la traducción se haya advertido por consola que no se encontraron ciertas palabras para poder hacer la traducción. En ese caso, el usuario tendrá que agregar manualmente lo que necesite para completar la cfg.

## 3. Demo

Para poder visualizar la demo se debe instalar el entorno como se indica en 1.3.1.

Una vez que se tiene el entorno correspondiente se debe abrir la consola y correr el siguiente comando desde el directorio raíz del repositorio:

```
pipenv run jupyterlab
```

Se abrirá jupyterlab en el navegador y desde allí hay que ingresar al archivo _demo.ipynv_

## 4. Testing

Para poder correr los test unitarios del código se debe instalar el entorno en modo desarrollo como se indica en 1.3.1.

Una vez que se tiene el entorno correspondiente se debe correr: 

```
pipenv run pytest/tests
```

En caso de estar trabajando en una colaboración para el repositorio estos test deben correrse antes de hacer la PR para saber si alguno falla. En caso de agregar nuevas funcionalidades se deberán subir también los nuevos test que correspondan. 
