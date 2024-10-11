import pymysql.cursors
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()
consulta_personas = """
    SELECT p.name_persones AS persones, r.namerols AS rol
    FROM persones p
    JOIN contingutcinematografic_persones cp ON p.idpersones = cp.id_persona
    JOIN rols r ON cp.id_rols = r.idrols
"""

cursor.execute(consulta_personas)
resultados = cursor.fetchall()

actores = [fila["persones"] for fila in resultados if fila["rol"] == "ACTOR"]
directores = [fila["persones"] for fila in resultados if fila["rol"] == "DIRECTOR"]
actores_directores = [fila["persones"] for fila in resultados if fila["rol"] == "ACTOR/DIRECTOR"]

total_actores = len(actores)
total_directores = len(directores)
total_actores_directores = len(actores_directores)

print("Total de actores:", total_actores)
print("Total de directores:", total_directores)
print("Total de actores/directores:", total_actores_directores)

cursor.close()
connection.close()

import matplotlib.pyplot as plt

# Datos
etiquetas = ['Actors/Directors', 'Directors', 'Actors']
sizes = [total_actores_directores, total_directores, total_actores]
colores = ['skyblue', 'lightgreen', 'lightcoral']

# Configuración del gráfico
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=etiquetas, autopct='%1.2f%%', startangle=140, colors=colores)
plt.title('Percentatge Actors/Directors, Directors i Actors')
plt.axis('equal')  # Para que el gráfico sea circular

# Mostrar gráfico
plt.show()
