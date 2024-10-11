import pandas as pd
import pymysql.cursors

fitxers = ['Prac1/Amazon_Prime_Titles.csv', 'Prac1/Disney_Plus_Titles.csv', 'Prac1/HBOMax_Titles.csv', 'Prac1/HuluTV_Titles.csv', 'Prac1/Netflix_Titles.csv', 'Prac1/ParamountTV_Titles.csv', 'Prac1/Rakuten_Viki_Titles.csv']
llista_continguts = []
llista_id = []

def comprobar_nan(valor):
    if pd.isna(valor):
        return True
    else:
        return False
    
def retornar_index(valor):
    valors = {
        "Amazon_Prime_Titles.csv": "1",
        "Disney_Plus_Titles.csv": "2",
        "HBOMax_Titles.csv": "3",
        "HuluTV_Titles.csv": "5",
        "Netflix_Titles.csv": "0",
        "ParamountTV_Titles.csv": "4",
        "Rakuten_Viki_Titles.csv": "6"
    }
    return valors.get(valor)

for fitxer in fitxers:
    contingut = pd.read_csv(fitxer)
    for  fila in contingut.itertuples():
        id_contingut = fila[1]
        title = fila[2]
        
        if id_contingut not in llista_id:
            llista_id.append(id_contingut)
            llista_continguts.append(fila)

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()
consulta = "INSERT INTO contingutcinematografic_plataforma (idcontingutCinematografic, idplataforma) VALUES (%s,%s)"

for fitxer in fitxers:
    contingut = pd.read_csv(fitxer)
    for peli_serie in llista_continguts:
        if comprobar_nan(peli_serie[3]):
            continue
        
        if comprobar_nan(peli_serie[5]):
            continue
        
        if comprobar_nan(peli_serie[7]):
            continue
        
        if comprobar_nan(peli_serie[2]):
            continue
        
        if pd.isna(peli_serie[12]) or pd.isna(peli_serie[13]):
            continue
        
        
        if peli_serie[1] in contingut['id'].values:
            valor = (peli_serie[1], retornar_index(fitxer))
            cursor.execute(consulta, valor)

connection.commit()
cursor.close()
connection.close()
        