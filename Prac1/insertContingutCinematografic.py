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
consulta = "INSERT INTO contingut_cinematografic (id_contingut_cinematografic, title_contingut_cinematografic, type_contingut_cinematografic, description_contingut_cinematografic, release_year_contingut_cinematografic, runtime_contingut_cinematografic, id_ac_contingut_cinematografic, id_tmbdcontingut_cinematografic, id_imbd, seasons_contingut_cinematografic) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
movie = 0
any = None
primaryKeyTMBD = 0
primaryKeyTMBDaux = 0
consultaAny = "SELECT idany_certificacio FROM any_certificacio WHERE name_any_certificacio = %s"
consultaTMB = "INSERT INTO tmbd (idtmbd, popularity_tmbd, score_tmbd) VALUES (%s,%s,%s)"

for peli_serie in llista_continguts:
    primaryKeyTMBDaux = primaryKeyTMBDaux + 1
    if pd.isna(peli_serie[6]):
        any = None
    else:
        valor_name_any_certificacio = peli_serie[6]
        cursor.execute(consultaAny, (valor_name_any_certificacio,))
        anyAux = cursor.fetchone()
        any = anyAux['idany_certificacio']
    if peli_serie[3] != "MOVIE":
        movie = 0
    else:
        movie = 1
    if pd.isna(peli_serie[14]) or pd.isna(peli_serie[15]):
        primaryKeyTMBD = None
    else:
        primaryKeyTMBD = primaryKeyTMBDaux
        valorTMBD = (str(primaryKeyTMBD), peli_serie[14],peli_serie[15])
        cursor.execute(consultaTMB, valorTMBD)
    
    
    seasons = peli_serie[10] if not pd.isna(peli_serie[10]) else None
    idmb = peli_serie[11] if not pd.isna(peli_serie[11]) else None
    description = peli_serie[4] if not pd.isna(peli_serie[4]) else None
    
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
    
    valor = (peli_serie[1], peli_serie[2], str(movie), description, peli_serie[5], peli_serie[7], any, primaryKeyTMBD ,idmb, seasons)
    primaryKeyTMBDaux = primaryKeyTMBDaux + 1

    print(valor)
    cursor.execute(consulta, valor)

connection.commit()
cursor.close()
connection.close()


