import pandas as pd
import pymysql.cursors

fitxers = ['Prac1/Amazon_Prime_Titles.csv', 'Prac1/Disney_Plus_Titles.csv', 'Prac1/HBOMax_Titles.csv', 'Prac1/HuluTV_Titles.csv', 'Prac1/Netflix_Titles.csv', 'Prac1/ParamountTV_Titles.csv', 'Prac1/Rakuten_Viki_Titles.csv']
llista_valors = []

for fitxer in fitxers:
    any = pd.read_csv(fitxer)
    for indice, fila in any.iterrows():
        anyCertificacio = fila.iloc[5]
        if anyCertificacio not in llista_valors and not pd.isna(anyCertificacio) :
            llista_valors.append(anyCertificacio)
print (llista_valors)


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()
consulta = "INSERT INTO any_certificacio (idany_certificacio, name_any_certificacio) VALUES (%s,%s)"
index = 0
for any in llista_valors:
    valor = (index, any)
    cursor.execute(consulta, valor)
    index = index + 1        

connection.commit()
cursor.close()
connection.close()