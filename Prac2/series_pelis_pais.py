import pymysql.cursors
import json

# Conexión a la base de datos
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()

# Consulta SQL para el número de series por país
consulta_series = """
SELECT 
    cp.name_paisos AS pais, 
    COUNT(*) AS num_series
FROM 
    contingut_cinematografic cc
JOIN 
    contingutcinematografic_paisos ccp ON cc.id_contingut_cinematografic = ccp.idcontingutCinematografic
JOIN 
    paisos cp ON ccp.id_paisos = cp.idpaisos
WHERE 
    cc.type_contingut_cinematografic = '1'
GROUP BY 
    cp.name_paisos
ORDER BY 
    cp.name_paisos;
"""

# Ejecutar la consulta de series
cursor.execute(consulta_series)

# Obtener los resultados de series
resultados_series = cursor.fetchall()

# Consulta SQL para el número de películas por país
consulta_peliculas = """
SELECT 
    cp.name_paisos AS pais, 
    COUNT(*) AS num_peliculas
FROM 
    contingut_cinematografic cc
JOIN 
    contingutcinematografic_paisos ccp ON cc.id_contingut_cinematografic = ccp.idcontingutCinematografic
JOIN 
    paisos cp ON ccp.id_paisos = cp.idpaisos
WHERE 
    cc.type_contingut_cinematografic = '0'
GROUP BY 
    cp.name_paisos
ORDER BY 
    cp.name_paisos;
"""

# Ejecutar la consulta de películas
cursor.execute(consulta_peliculas)

# Obtener los resultados de películas
resultados_peliculas = cursor.fetchall()

# Combinar los resultados de series y películas por país
resultados_combinados = {}
for resultado_serie in resultados_series:
    pais = resultado_serie['pais']
    resultados_combinados[pais] = {'num_series': resultado_serie['num_series']}

for resultado_pelicula in resultados_peliculas:
    pais = resultado_pelicula['pais']
    if pais in resultados_combinados:
        resultados_combinados[pais]['num_peliculas'] = resultado_pelicula['num_peliculas']
    else:
        resultados_combinados[pais] = {'num_peliculas': resultado_pelicula['num_peliculas']}

# Completar los países que no tienen películas o series con 0
for pais in resultados_combinados.keys():
    if 'num_series' not in resultados_combinados[pais]:
        resultados_combinados[pais]['num_series'] = 0
    if 'num_peliculas' not in resultados_combinados[pais]:
        resultados_combinados[pais]['num_peliculas'] = 0

# Mostrar los resultados por consola
for pais, datos in resultados_combinados.items():
    num_series = datos.get('num_series', 0)
    num_peliculas = datos.get('num_peliculas', 0)
    print(f"País: {pais}, Número de series: {num_series}, Número de películas: {num_peliculas}")

# Cerrar el cursor y la conexión
cursor.close()
connection.close()

# Guardar los resultados en un archivo JSON
with open('num_series_y_peliculas_por_pais.json', 'w', encoding='utf-8') as file:
    json.dump(resultados_combinados, file, ensure_ascii=False, indent=4)

print("Los resultados se han guardado en num_series_y_peliculas_por_pais.json")
