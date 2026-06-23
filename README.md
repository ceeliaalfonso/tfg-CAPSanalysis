# tfg-CAPSanalysis
# Documentación del Repositorio: Procesamiento de datos meteorológicos y análisis de CAPs.
 # 1. Descripción General del Proyecto
Este repositorio contiene los datos de entrada, los scripts de procesamiento y los archivos de salida correspondientes al estudio comparativo entre las estaciones meteorológicas de Villaceid y Villayuste. El objetivo principal de la investigación es la identificación, filtrado y caracterización de los fenómenos de piscina de aire frío (CAP, por sus siglas en inglés) registrados en la zona junto con la posterior estimación de las aportaciones hídricas derivadas, así como una revisión de la bibliografía actual para comprender los posibles efectos a nivel ambiental que puedan derivarse de los resultados del análisis.

Se utilizó el programa Python para automatizar la homogeneización de los datos de entrada. Además, se aplican criterios de continuidad temporal para agrupar cada evento como una unidad.

 # 2. Origen y Naturaleza de los Datos de Entrada
Los datos meteorológicos de partida proceden de dos estaciones distintas y presentan características estructurales incompatibles debido a que vienen de distintas fuentes:

Estación de Villaceid
Los datos correspondientes a esta localización fueron proporcionados por la Asociación Meteorológica del Noroeste Peninsular (NOROMET) y se almacenan en la carpeta "Datos villaceid". Esta carpeta contiene los registros en su estado original, tal y como fueron extraídos del sistema de adquisición de datos de la estación, manteniendo la resolución temporal y el formato nativo sin modificaciones previas.

Estación de Villayuste
Los datos de esta estación se encuentran en la carpeta "villayuste". A diferencia de la estación anterior, estos registros requirieron una intervención manual previa. Estos datos provienen de la plataforma web Weather Underground, la cual mostraba los registros en archivos diarios y no permitía la descarga directa de series temporales continuas, por ello fue necesario compilar los datos de manera manuscrita, agrupándolos en un archivo por mes.

  # 3. Metodología de Procesamiento y Flujo de Trabajo
El análisis de la información se dividió en dos procesos independientes, motivadas por la evolución de las necesidades del trabajo.

#     Fase I: Identificación y Clasificación de Eventos de Inversión Térmica
La primera etapa tenía como objetivo homogeneizar los datos para después identificar los eventos de CAP como unidades conjuntas de datos de inversión térmica continuada. 
Para procesar esta fase, se desarrolló una estructura de doce scripts de Python idénticos, donde cada uno tenía dos archivos de entrada y se encargaba de analizar un mes específico del año. Por ejemplo; para el mes de julio se parte de los archivos "JULIO25_VILLACEID.xlsx" y "JULIO25_VILLAYUSTE.xlsx" (los mismos datos brutos presentados en este repositorio, pero renombrados de cara a facilitar su manejo) y se aplica el script de python "análisis_eventos_julio.py". Este código consta de tres fases en su estructura, delas cuales la primera  esta dedicada a homogeneizar la temporalidad de los datos, estableciendo un grid con frecuencia de 30 minutos para mostrar los datos de ambas estaciones con la misma temporalidad. La segunda parte del código compara los registros de temperatura de villaceid y de villayuste y elimina aquellos en que no se cumpla que la Tº de Villaceid es menor que la Tº de Villayuste (inversión térmica). Como último paso, al ejecutarlo se agrupan también los datos continuos en el tiempo como parte de un mismo evento, generando a su vez columnas con datos propios como la duración del evento o su inversión máxima.

El algoritmo ejecuta los siguientes pasos de manera secuencial:

Lectura de las fuentes de datos de ambas estaciones.

Sincronización y homogeneización de la serie temporal en intervalos fijos de 30 minutos. Es importante destacar que el script no realiza promedios aritméticos; extrae el dato puntual registrado en cada fracción horaria para preservar la fidelidad de los extremos térmicos.

Aplicación de un filtro condicional para conservar únicamente los registros que cumplen la premisa térmica del estudio.

Agrupación de los registros resultantes en función de su continuidad temporal, definiendo de este modo el inicio, la duración y el fin de cada evento de inversión individual.

Cada uno de los doce scripts generaba un archivo de salida intermedio en formato de hoja de cálculo (por ejemplo, eventos_julio.xlsx). Dichos archivos mensuales no se han incluido en el repositorio para evitar la redundancia de datos. En su lugar, se procedió a la consolidación de los doce periodos en un único documento maestro final, el cual se encuentra disponible bajo el nombre de EVENTOS.xlsx.

#     Fase II: Extracción Continua para Cálculos de Aportaciones Hídricas
Durante una etapa posterior del estudio, las directrices de la investigación requirieron analizar las aportaciones hídricas del fenómeno. Para realizar estos cálculos termodinámicos de manera estadísticamente correcta, se determinó que la segmentación por eventos de la Fase I resultaba inadecuada, siendo indispensable disponer de una serie temporal continua cada 30 minutos sin interrupciones por agrupación.

Para dar solución a este requerimiento, se diseñó un nuevo flujo de trabajo que volvía a tomar como punto de partida los datos brutos originales de las estaciones. El procesamiento automatizado se implementó en el script titulado filtrar_30min.py. Este código se encarga de realizar la lectura, la sincronización en intervalos de media hora y el filtrado térmico elemental, exportando los resultados directamente.

El documento resultante de este script fue sometido a una fase de depuración y enriquecimiento analítico fuera del entorno de desarrollo de Python. Utilizando software de hoja de cálculo, se realizaron las siguientes acciones:

Revisión manual exhaustiva para identificar y eliminar aquellos registros que, por anomalías o factores del entorno, no se correspondían con una inversión térmica real.

Introducción de formulación matemática adicional para calcular los valores correspondientes al punto de rocío.

Integración de las ecuaciones necesarias para la determinación cuantitativa de las aportaciones hídricas.

El producto final de esta segunda fase se encuentra almacenado en el repositorio bajo el nombre de INVERSIONES_ESCARCHA.xlsx.

#   4. Inventario de Componentes del Repositorio
A modo de síntesis, los elementos que configuran la estructura de este proyecto se describen a continuación:

  Directorio de datos de Villaceid:Almacena las series temporales climáticas originales y sin procesar de dicha estación.

  Directorio de datos de Villayuste: Aloja la información climática de la estación homónima, estructurada manualmente en periodos mensuales debido a restricciones de la fuente web.

  análisis_eventos_julio.py: Archivo escrito en Python que sirve de ejemplo metodológico para el filtrado de cada mes, la igualación temporal a 30 minutos y la delimitación de eventos por continuidad física.

  EVENTOS.xlsx: Archivo en formato Excel que unifica los resultados de los doce meses del año obtenidos mediante el proceso de la Fase I.

  Filtrar_30min.py: Código en Python desarrollado para la extracción sistemática de los datos cada 30 minutos sin aplicar criterios de agrupación por eventos.
  
  INVERSIONES_ESCARCHA.xlsx: Archivo consolidado en formato Excel que contiene la serie de inversión depurada manualmente, complementada con los cálculos analíticos de punto de rocío y aportaciones hídricas.
