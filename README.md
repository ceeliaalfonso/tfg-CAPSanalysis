# tfg-CAPSanalysis
# Documentación del Repositorio: Procesamiento de datos meteorológicos y análisis de CAPs.
 # 1. Descripción General del Proyecto
Este repositorio contiene los datos de entrada, los scripts de procesamiento y los archivos de salida correspondientes al estudio comparativo entre las estaciones meteorológicas de Villaceid y Villayuste. El objetivo principal de la investigación es la identificación, filtrado y caracterización de los fenómenos de piscina de aire frío (CAP, por sus siglas en inglés) registrados en la zona junto con la posterior estimación de las aportaciones hídricas derivadas, así como una revisión de la bibliografía actual para comprender los posibles efectos a nivel ambiental que puedan derivarse de los resultados del análisis.

Se utilizó el programa Python para automatizar la homogeneización de los datos de entrada. Además, se aplican criterios de continuidad temporal para agrupar cada evento como una unidad.

 # 2. Origen y Naturaleza de los Datos de Entrada
Los datos meteorológicos de partida proceden de dos estaciones distintas y presentan características estructurales incompatibles debido a que vienen de distintas fuentes:

Estación de Villaceid
Los datos correspondientes a esta localización fueron proporcionados por la Asociación Meteorológica del Noroeste Peninsular (NOROMET) y se almacenan en la carpeta "Villaceid". Esta carpeta contiene los registros en su estado original, tal y como fueron extraídos del sistema de adquisición de datos de la estación, manteniendo la resolución temporal y el formato nativo sin modificaciones previas.

Estación de Villayuste
Los datos de esta estación se encuentran en la carpeta "villayuste". A diferencia de la estación anterior, estos registros requirieron una intervención manual previa. Estos datos provienen de la plataforma web Weather Underground, la cual mostraba los registros en archivos diarios y no permitía la descarga directa de series temporales continuas, por ello fue necesario compilar los datos de manera manuscrita, agrupándolos en un archivo por mes.

  # 3. Metodología de Procesamiento y Flujo de Trabajo
El análisis de la información se dividió en dos procesos independientes, motivadas por la evolución de las necesidades del trabajo.

#     Fase I: Identificación y Clasificación de Eventos de Inversión Térmica
La primera etapa tenía como objetivo homogeneizar los datos para después identificar los eventos de CAP como unidades conjuntas de datos de inversión térmica continuada. 
Para procesar esta fase, se desarrolló una estructura de doce scripts de Python idénticos, donde cada uno tenía dos archivos de entrada y se encargaba de analizar un mes específico del año. Por ejemplo; para el mes de julio se parte de los archivos "JULIO25_VILLACEID.xlsx" y "JULIO25_VILLAYUSTE.xlsx" (los mismos datos brutos presentados en este repositorio, pero renombrados de cara a facilitar su manejo) y se aplica el script de python "análisis_eventos_julio.py". Este código consta de tres fases en su estructura, delas cuales la primera  esta dedicada a homogeneizar la temporalidad de los datos, estableciendo un grid con frecuencia de 30 minutos para mostrar los datos de ambas estaciones con la misma temporalidad. La segunda parte del código compara los registros de temperatura de villaceid y de villayuste y elimina aquellos en que no se cumpla que la Tº de Villaceid es menor que la Tº de Villayuste (inversión térmica). Como último paso, al ejecutarlo se agrupan también los datos continuos en el tiempo como parte de un mismo evento, generando a su vez columnas con datos propios como la duración del evento o su inversión máxima.

El código "análisis_eventos_julio.py" ejecuta los siguientes pasos de manera secuencial:

1º Lectura de las fuentes de datos de ambas estaciones.

2º Homogeneización de la serie temporal en intervalos fijos de 30 minutos. Es importante destacar que el script no realiza promedios aritméticos; extrae el dato más cercano registrado para preservar la fidelidad de los datos.

3º Aplicación de un filtro condicional para conservar únicamente los registros que cuentan con inversión térmica (Tª en Villaceid menor que Tª Villayuste.

4º Agrupación de los registros continuados como un mismo evento, creando un archivo donde cada fila es un evento. Este archivo contiene columnas de datos con fecha y hora de inicio y fin, duración y diferencia máxima de temperatura.

Cada uno de los doce scripts generaba un archivo de salida en formato de hoja de cálculo (por ejemplo, eventos_julio.xlsx). Dichos archivos mensuales no se han incluido en el repositorio para evitar la redundancia de datos. En su lugar, se adjunta un único documento final con estos archivos agrupados, nombrado como "EVENTOS.xlsx".

#     Fase II: Extracción de datos continuos para cálculos de aportaciones hídricas
En la siguiente etapa se utilizaron de nuevo los mismos datos de entrada, pero los siguientes objetivos del estudio se necesitó un nuevo procesado de los datos, donde los datos de salida mostraran los datos continuos sin la posterior agrupación por eventos.
Se utilizó el código "filtrar_30min.py", homogeneizando los datos de entrada con el mismo intervalo de 30 minutos, también sin hacer promedios y luego cribando los datos para solo quedarnos con aquellos que presentaban inversión térmica. En este caso, el documento de salida presentaba columnas de datos puntuales como la fecha y hora, humedad relativa, temperatura, velocidad del viento, precipitacion, etc. Además, a partir de estos datos se calculó el punto de rocío y el tipo de aportación hídrica esperada, resultando en el archivo adjunto "INVERSIONES_ESCARCHA.xlsx".

#   4. Inventario
A modo de síntesis, los archivos en el repositorio se describen a continuación:

  Villaceid: Carpeta que contiene los archivos, tipo .csv, con los datos brutos medidos por la estación meteorológica durante el año 2025.

  Villayuste: Carpeta con los archivos, tipo .xlsx, con los datos ya agrupados, mostrando un archivo por cada mes.

  análisis_eventos_julio.py: Código para Python que sirve de ejemplo metodológico para el filtrado de cada mes, establece una serie temporal de 30 minutos y la define los eventos por continuidad de los registros.

  EVENTOS.xlsx: Archivo en formato .xlsx que unifica los resultados de los doce meses del año obtenidos mediante el proceso de la Fase I.

  Filtrar_30min.py: Código en Python para la homogeneización de los datos a intervalos de 30 minutos, sin aplicar criterios de agrupación por eventos.
  
  INVERSIONES_ESCARCHA.xlsx: Archivo resultante de la Fase II en formato .xlsx que contiene los registros con inversión térmica y sus datos medidos en ambas estaciones. Contiene además los cálculos analíticos de punto de rocío y aportaciones hídricas.
