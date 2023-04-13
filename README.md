# Homologación de Universidades
Este script de Python permite la homologación de universidades en base a los comentarios de un archivo de muestra y los nombres de universidades contenidos en un archivo de referencia. Para ello, se utilizan dos métodos de homologación que permiten identificar los nombres de universidades que aparecen en los comentarios del archivo de muestra.

# Requerimientos
Este script utiliza las siguientes librerías de Python (versión 3.7.9) :

* pandas
* json

# Uso
Para utilizar este script, debes seguir los siguientes pasos:

1. Descargar los archivos instituciones_educativas.csv y Universidades.json que contienen los datos de muestra y de referencia, respectivamente, y colocarlos en el mismo directorio donde se encuentra el script.
2. Ejecutar el script homologacion_universidades.py.
3. El resultado de la homologación se guarda en un archivo homologacion.csv que se crea automáticamente en el mismo directorio donde se encuentra el script.

# Métodos de homologación
El script utiliza los siguientes métodos de homologación:

1. Método 1: Validación entre siglas de las universidades en el archivo de referencia y los comentarios que poseen siglas en su estructura. Este método permite identificar las universidades a partir de las siglas contenidas en los comentarios del archivo de muestra.

2. Método 2: Validación entre los comentarios sin stop words y los nombres de las universidades en el archivo de referencia. Este método permite identificar las universidades a partir de las palabras contenidas en los comentarios del archivo de muestra.

# Resultados
El script genera un archivo homologacion.csv que contiene los comentarios del archivo de muestra, junto con la universidad homologada a partir de los métodos de homologación. Además, se exporta un archivo universidades.csv que contiene la lista de universidades homologadas y sus sinónimos (los diferentes nombres con los que aparecen en el archivo de muestra).
