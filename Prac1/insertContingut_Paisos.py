import pandas as pd
import pymysql.cursors

fitxers = ['Prac1/Amazon_Prime_Titles.csv', 'Prac1/Disney_Plus_Titles.csv', 'Prac1/HBOMax_Titles.csv', 'Prac1/HuluTV_Titles.csv', 'Prac1/Netflix_Titles.csv', 'Prac1/ParamountTV_Titles.csv', 'Prac1/Rakuten_Viki_Titles.csv']
llista_continguts = []
llista_id = []
pais_totals = []
paisaux = None

consultaPais = "SELECT idpaisos FROM paisos WHERE name_paisos = %s"
consulta = "INSERT INTO contingutcinematografic_paisos (idcontingutCinematografic, id_paisos) VALUES (%s,%s)"

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()

def comprobar_nan(valor):
    if pd.isna(valor):
        return True
    else:
        return False
    


for fitxer in fitxers:
    contingut = pd.read_csv(fitxer)
    for  fila in contingut.itertuples():
        id_contingut = fila[1]
        title = fila[2]
        
        if id_contingut not in llista_id:
            llista_id.append(id_contingut)
            llista_continguts.append(fila)

for peli_serie in llista_continguts:
    pais_totals.clear()
    
    if comprobar_nan(peli_serie[3]):
        continue
        
    if comprobar_nan(peli_serie[5]):
        continue
        
    if comprobar_nan(peli_serie[7]):
        continue
        
    if comprobar_nan(peli_serie[2]):
        continue
        
    if comprobar_nan(peli_serie[8]):
        continue
        
    if pd.isna(peli_serie[12]) or pd.isna(peli_serie[13]):
        continue
        
    if isinstance(peli_serie[9], str):
        pais = peli_serie[9].split(',')
        pais = [pa.strip().strip("[]").strip("'") for pa in pais]
        pais_totals.extend(pais)
        pais_totals = list(set(pais_totals))
        
        for pais in pais_totals:
            cursor.execute(consultaPais, (pais))
            idPais = cursor.fetchone()
            if idPais is None:
                continue           
            paisaux = idPais['idpaisos']
            valor = (peli_serie[1], str(paisaux))
            cursor.execute(consulta,valor)
            
connection.commit()
cursor.close()
connection.close()
        
        