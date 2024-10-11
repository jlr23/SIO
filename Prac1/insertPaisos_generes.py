import pandas as pd
import pymysql.cursors

fitxers = ['Prac1/Amazon_Prime_Titles.csv', 'Prac1/Disney_Plus_Titles.csv', 'Prac1/HBOMax_Titles.csv', 'Prac1/HuluTV_Titles.csv', 'Prac1/Netflix_Titles.csv', 'Prac1/ParamountTV_Titles.csv', 'Prac1/Rakuten_Viki_Titles.csv']


generes_totals = []
paisos_totals = []
for fitxer in fitxers:
    pelis = pd.read_csv(fitxer)
    for indice, fila in pelis.iterrows():
        dada_columna_7 = fila.iloc[7]
        dada_columna_8 = fila.iloc[8]
        
        if isinstance(dada_columna_7, str):
            generes = dada_columna_7.split(',')
            generes = [gen.strip().strip("[]").strip("'") for gen in generes]
            generes_totals.extend(generes)
        
        if isinstance(dada_columna_8, str):
            pais = dada_columna_8.split(',')
            pais = [pa.strip().strip("[]").strip("'") for pa in pais]
            paisos_totals.extend(pais)

generes_totals = list(set(generes_totals))
generes_totals.remove('')
paisos_totals = list(set(paisos_totals))
paisos_totals.remove('')

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
print("Afegint generes...")
cursor = connection.cursor()
consulta = "INSERT INTO genere (idgenere, name_genere) VALUES (%s,%s)"
index = 0
for gen in generes_totals:
    valor = (index, gen)
    cursor.execute(consulta, valor)
    index = index + 1
print("Generes afegits")

print("Afegint paisos...")
consulta = "INSERT INTO paisos (idpaisos, name_paisos) VALUES (%s,%s)"
index = 0
for pais in paisos_totals:
    valor = (index, pais)
    cursor.execute(consulta, valor)
    index = index +1
print("Paisos afegits")

connection.commit()
cursor.close()
connection.close()

