import pymysql.cursors
import pandas as pd
import json

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()

consulta="""
SELECT 
    cp.name_paisos AS pais, 
    AVG(i.score_imbd) AS media_score_imbd
FROM 
    contingut_cinematografic cc
JOIN 
    imbd i ON cc.id_imbd = i.idimbd
JOIN 
    contingutcinematografic_paisos ccp ON cc.id_contingut_cinematografic = ccp.idcontingutCinematografic
JOIN 
    paisos cp ON ccp.id_paisos = cp.idpaisos
GROUP BY 
    cp.name_paisos
ORDER BY 
    cp.name_paisos;
"""

# Ejecutar la consulta
cursor.execute(consulta)

# Obtener los resultados
resultados = cursor.fetchall()

# Mostrar los resultados por consola
for resultado in resultados:
    print(f"País: {resultado['pais']}, Media de score_imbd: {resultado['media_score_imbd']:.2f}")

# Cerrar el cursor y la conexión
cursor.close()
connection.close()

# Guardar los resultados en un archivo JSON
with open('media_score_imbd_por_pais.json', 'w', encoding='utf-8') as file:
    json.dump(resultados, file, ensure_ascii=False, indent=4)

print("Los resultados se han guardado en media_score_imbd_por_pais.json")