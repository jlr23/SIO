import pandas as pd
import pymysql.cursors

fitxers = ['Prac1/Amazon_Prime_Titles.csv', 'Prac1/Disney_Plus_Titles.csv', 'Prac1/HBOMax_Titles.csv', 'Prac1/HuluTV_Titles.csv', 'Prac1/Netflix_Titles.csv', 'Prac1/ParamountTV_Titles.csv', 'Prac1/Rakuten_Viki_Titles.csv']
llista_valors = []
diccionari_ids = {}
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()
consulta = "INSERT INTO imbd (idimbd, score_imbd, votes_imbd) VALUES (%s,%s,%s)"
for fitxer in fitxers:
    imbd = pd.read_csv(fitxer)
    print (fitxer)
    for indice, fila in imbd.iterrows():
        imbd_id = fila.iloc[10]
        imbd_score = fila.iloc[11]
        imbd_votes = fila.iloc[12]
        if pd.isna(imbd_id) or pd.isna(imbd_score) or pd.isna(imbd_votes):
            continue
        else:
            if imbd_id not in diccionari_ids:
                diccionari_ids[imbd_id] = True
                llista_valors.append((imbd_id, str(imbd_score), imbd_votes))

for valor in llista_valors:
    cursor.execute(consulta, valor)
            

connection.commit()
cursor.close()
connection.close()