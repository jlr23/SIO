import pymysql.cursors

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()
consulta = "INSERT INTO plataforma (idplataforma,name_plataforma) VALUES (%s,%s)"
valor = (0, 'Netflix')
cursor.execute(consulta, valor)
valor = (1, 'Amazon Prime')
cursor.execute(consulta, valor)
valor = (2,'Disney Plus')
cursor.execute(consulta, valor)
valor = (3, 'HBOMax')
cursor.execute(consulta, valor)
valor = (4, 'ParamountTV')
cursor.execute(consulta, valor)
valor = (5, 'HuluTV')
cursor.execute(consulta, valor)
valor = (6, 'Rakuten Viki')
cursor.execute(consulta, valor)
connection.commit()
print('Plataformes afegides')

consulta = "INSERT INTO rols (idrols, namerols) VALUES (%s,%s)"
valor = (0, 'ACTOR')
cursor.execute(consulta, valor)
valor = (1,'DIRECTOR')
cursor.execute(consulta, valor)
valor = (2, 'ACTOR/DIRECTOR')
cursor.execute(consulta, valor)
connection.commit()
print('Rols afegits')

cursor.close()
connection.close()

