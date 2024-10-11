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

consulta_actores_mes_pelis = """
    SELECT p.name_persones AS actor,
    COUNT(cp.id_contingutCinematografic) AS total_pelis
    FROM persones p
    JOIN contingutcinematografic_persones cp ON p.idpersones = cp.id_persona
    JOIN rols r ON cp.id_rols = r.idrols
    WHERE r.namerols IN ('ACTOR', 'ACTOR/DIRECTOR')
    GROUP BY p.name_persones
    ORDER BY total_pelis DESC
    LIMIT 10;
"""
cursor.execute(consulta_actores_mes_pelis)
actores_mas_pelis = cursor.fetchall()

cursor.close()
connection.close()

if actores_mas_pelis:
    print("Els deu ACTOR i ACTOR/DIRECTOR amb més aparicions en pel·lícules són:")
    for fila in actores_mas_pelis:
        actor = fila['actor']
        total_pelis = fila['total_pelis']
        print(f"Actor: {actor}, Total de pel·lícules: {total_pelis}")
else:
    print("No hi ha resultats.")

#part grafica
dades=pd.DataFrame(actores_mas_pelis)
sns.barplot(data=dades, x='total_pelis', y='actor', palette='viridis')
plt.xlabel('Total pel.licules')
plt.ylabel('Actor')
plt.title('Actors amb més participació a pel.licules')
plt.tight_layout()
plt.savefig("graficConsulta3.png")
plt.show()