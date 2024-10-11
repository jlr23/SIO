import pymysql.cursors

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
    cc.title_contingut_cinematografic,
    GROUP_CONCAT(p.name_plataforma SEPARATOR ', ') AS plataformas_disponibles
FROM 
    contingut_cinematografic cc
JOIN 
    contingutcinematografic_plataforma cp ON cc.id_contingut_cinematografic = cp.idcontingutCinematografic
JOIN 
    plataforma p ON cp.idplataforma = p.idplataforma
WHERE 
    cc.title_contingut_cinematografic = 'The Lucky Texan';


"""

cursor.execute(consulta)
plataformes_contingut_accio = cursor.fetchall()

cursor.close()
connection.close()

print (plataformes_contingut_accio)