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

# Consulta SQL para seleccionar los dos actores con más países diferentes
consulta_top_actores = """
SELECT 
    p.idpersones,
    p.name_persones AS actor,
    COUNT(DISTINCT cp.idpaisos) AS num_paises
FROM 
    persones p
JOIN 
    contingutcinematografic_persones cpp ON p.idpersones = cpp.id_persona
JOIN 
    contingut_cinematografic cc ON cpp.id_contingutCinematografic = cc.id_contingut_cinematografic
JOIN 
    contingutcinematografic_paisos ccp ON cc.id_contingut_cinematografic = ccp.idcontingutCinematografic
JOIN 
    paisos cp ON ccp.id_paisos = cp.idpaisos
GROUP BY 
    p.idpersones, p.name_persones
ORDER BY 
    num_paises DESC
LIMIT 2;
"""

# Ejecutar la consulta para obtener los dos actores con más países diferentes
cursor.execute(consulta_top_actores)
top_actores = cursor.fetchall()

# Obtener los IDs de los dos actores seleccionados
actor_ids = [actor['idpersones'] for actor in top_actores]

# Consulta SQL para obtener los países y años para los dos actores seleccionados
consulta_paises_anyos = """
SELECT 
    p.name_persones AS actor,
    cp.name_paisos AS pais,
    cc.release_year_contingut_cinematografic AS anyo
FROM 
    persones p
JOIN 
    contingutcinematografic_persones cpp ON p.idpersones = cpp.id_persona
JOIN 
    contingut_cinematografic cc ON cpp.id_contingutCinematografic = cc.id_contingut_cinematografic
JOIN 
    contingutcinematografic_paisos ccp ON cc.id_contingut_cinematografic = ccp.idcontingutCinematografic
JOIN 
    paisos cp ON ccp.id_paisos = cp.idpaisos
WHERE 
    p.idpersones IN (%s, %s)
ORDER BY 
    p.name_persones, cc.release_year_contingut_cinematografic;
""" % (actor_ids[0], actor_ids[1])

# Ejecutar la consulta para obtener los países y años para los dos actores seleccionados
cursor.execute(consulta_paises_anyos)
results = cursor.fetchall()

# Agrupar resultados por actor
actors_data = {}
for row in results:
    actor = row['actor']
    pais = row['pais']
    anyo = row['anyo']
    if actor not in actors_data:
        actors_data[actor] = []
    actors_data[actor].append({'pais': pais, 'anyo': anyo})

# Mostrar resultados
for actor, trabajos in actors_data.items():
    print(f"Actor: {actor}")
    for trabajo in trabajos:
        print(f"  País: {trabajo['pais']}, Año: {trabajo['anyo']}")
    print()

# Guardar en JSON
with open('actores_paises_anyos.json', 'w') as json_file:
    json.dump(actors_data, json_file, indent=4)

cursor.close()
connection.close()
