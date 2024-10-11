import pandas as pd
import pymysql.cursors

persones = pd.read_csv('Prac1/persones.csv')
personesS = persones.drop_duplicates(subset=[persones.columns[0]])
print(persones)

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
print("Insertant persones...")
cursor = connection.cursor()
consulta = "INSERT INTO persones (idpersones, name_persones) VALUES (%s,%s)"
for indice, fila in personesS.iterrows():
    dada_columna_0 = fila.iloc[0]
    dada_columna_2 = fila.iloc[2]
    valor = (dada_columna_0,dada_columna_2)
    if pd.isna(dada_columna_0) or pd.isna(dada_columna_2):
        continue
    cursor.execute(consulta, valor)

connection.commit()
cursor.close()
connection.close()
print("\nPersones afegides")
