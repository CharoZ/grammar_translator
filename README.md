# grammar_translator

## 1. Instalaciòn

### 1.1. Python y pip

Para poder utilizar el repositorio con el entorno que le corresponde es necesario tener instalada alguna versiòn de python 3.8 en la computadora. A su vez es necesario contar con pip instalado. En caso de no tenerlo, se debe instalar de la siguiente forma: 

```
sudo apt install python3-pip
```

### 1.2. Instalaciòn pipenv

Para acceder al entorno que fue creado para el repositorio se debe instalar la librerìa pipenv
```
pip3 install pipenv
```

### 1.3. Creaciòn del entorno

Una vez que todo estè instalado, hay que moverse al directorio raìz del repositorio y correr el siguiente comando:

```
pipenv install
```

Esto crearà el entorno con todas las dependencias necesarias para poder usar el còdigo. Dentro de este entorno se encuentra instalado este repositorio como un paquete, es decir, puede importarse del siguiente modo:

```
import grammar_translator as gt
```