import pymysql.cursors
import pandas as pd
import json
from decimal import Decimal

# Conexión a la base de datos
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()

# Consulta SQL para obtener el contenido total por país y el género predominante
consulta = """
WITH TotalContenidos AS (
    SELECT cp.name_paisos AS pais, COUNT(*) AS total_contenido
    FROM contingut_cinematografic cc
    JOIN contingutcinematografic_paisos cpc ON cc.id_contingut_cinematografic = cpc.idcontingutCinematografic
    JOIN paisos cp ON cpc.id_paisos = cp.idpaisos
    GROUP BY cp.name_paisos
),
GeneroPredominante AS (
    SELECT cp.name_paisos AS pais, g.name_genere AS genere, COUNT(*) AS count_genere
    FROM contingut_cinematografic cc
    JOIN contingutcinematografic_paisos cpc ON cc.id_contingut_cinematografic = cpc.idcontingutCinematografic
    JOIN paisos cp ON cpc.id_paisos = cp.idpaisos
    JOIN contingutcinematografic_genere ccg ON cc.id_contingut_cinematografic = ccg.idcontingutCinematografic
    JOIN genere g ON ccg.idgenere = g.idgenere
    GROUP BY cp.name_paisos, g.name_genere
    HAVING COUNT(*) = (
        SELECT MAX(count_genere)
        FROM (
            SELECT cp2.name_paisos, g2.name_genere, COUNT(*) AS count_genere
            FROM contingut_cinematografic cc2
            JOIN contingutcinematografic_paisos cpc2 ON cc2.id_contingut_cinematografic = cpc2.idcontingutCinematografic
            JOIN paisos cp2 ON cpc2.id_paisos = cp2.idpaisos
            JOIN contingutcinematografic_genere ccg2 ON cc2.id_contingut_cinematografic = ccg2.idcontingutCinematografic
            JOIN genere g2 ON ccg2.idgenere = g2.idgenere
            GROUP BY cp2.name_paisos, g2.name_genere
        ) AS subquery
        WHERE subquery.name_paisos = cp.name_paisos
    )
)
SELECT 
    gp.pais, 
    gp.genere, 
    gp.count_genere, 
    tc.total_contenido, 
    (gp.count_genere / tc.total_contenido) * 100 AS porcentaje
FROM 
    GeneroPredominante gp
JOIN 
    TotalContenidos tc ON gp.pais = tc.pais
ORDER BY 
    gp.pais;
"""

# Ejecutar la consulta
cursor.execute(consulta)
resultados = cursor.fetchall()

# Convertir los valores Decimal a float
for resultado in resultados:
    for key, value in resultado.items():
        if isinstance(value, Decimal):
            resultado[key] = float(value)

# Convertir los resultados a un DataFrame
df = pd.DataFrame(resultados, columns=['pais', 'genere', 'count_genere', 'total_contenido', 'porcentaje'])

# Mostrar los resultados por pantalla
print(df)

# Convertir el DataFrame a un diccionario
resultados_dict = df.to_dict(orient='records')

# Guardar el diccionario en un archivo JSON
with open('resultados.json', 'w', encoding='utf-8') as file:
    json.dump(resultados_dict, file, ensure_ascii=False, indent=4)

print("Los resultados se han guardado en resultados.json")

# Cerrar la conexión
cursor.close()
connection.close()
