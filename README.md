# tfg-CAPSanalysis
# Documentación del Repositorio: Procesamiento de Datos Meteorológicos y Análisis de Inversiones Térmicas
 # 1. Descripción General del Proyecto
Este repositorio contiene el conjunto de datos, los scripts de procesamiento y los resultados finales correspondientes al estudio climático comparativo entre las estaciones meteorológicas de Villaceid y Villayuste. El objetivo principal de la investigación es la identificación, filtrado y caracterización de los fenómenos de inversión térmica entre ambas localizaciones, así como la posterior estimación de las aportaciones hídricas derivadas.

A través de los módulos de programación incluidos, se automatiza la homogeneización de series temporales de origen heterogéneo y se aplican criterios de continuidad física para aislar los eventos meteorológicos de interés. El flujo de trabajo responde a las necesidades analíticas surgidas durante las distintas fases del estudio, transitando desde una perspectiva orientada a eventos aislados hacia un análisis continuo de la masa de aire y su humedad.

 # 2. Origen y Naturaleza de los Datos de Entrada
Los datos meteorológicos de partida proceden de dos estaciones distintas y presentan características estructurales diferenciadas debido a las limitaciones de descarga de las plataformas de origen:

Estación de Villaceid
Los datos correspondientes a esta localización se almacenan en el directorio denominado datos villaceid. Esta carpeta contiene los registros meteorológicos en su estado bruto original, tal y como fueron extraídos del sistema de adquisición de datos de la estación, manteniendo la resolución temporal y el formato nativo sin modificaciones previas.

Estación de Villayuste
Los datos de esta estación se encuentran en la carpeta villayuste. A diferencia de la estación anterior, estos registros requirieron una intervención manual previa a su incorporación al repositorio. Debido a que la interfaz web de origen limitaba la consulta a una visualización diaria y no permitía la descarga directa de series temporales continuas, fue necesario compilar y estructurar los datos de manera manuscrita, agrupándolos en archivos de periodicidad mensual para posibilitar su posterior tratamiento informático.

  # 3. Metodología de Procesamiento y Flujo de Trabajo
El análisis de la información se dividió en dos fases metodológicas independientes, motivadas por la evolución de las necesidades del estudio de investigación.

#     Fase I: Identificación y Clasificación de Eventos de Inversión Térmica
En la primera etapa del proyecto, el interés se centró en aislar aquellos periodos de tiempo específicos en los que se manifestaba un fenómeno de inversión térmica entre ambas estaciones. Para que un periodo fuera considerado como tal, debía cumplir con la condición física de que la temperatura registrada en la estación de Villaceid fuera estrictamente inferior a la registrada en Villayuste.

Para procesar esta fase, se desarrolló una estructura de doce scripts de Python idénticos, donde cada uno se encargaba de analizar un mes específico del año. Con el propósito de simplificar la arquitectura del repositorio y facilitar su comprensión, se ha subido un único script como modelo representativo: analisis_eventos_julio.py.

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
