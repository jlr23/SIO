# Funció per obtenir l'opció de l'usuari
def mostrar_lote(filas, inicio, fin):
    for i in range(inicio, fin):
        if i < len(filas):
            fila = filas[i]
            print("------------------------------------------------------")
            print(f"Títol: {fila['title_contingut_cinematografic']}")
            print(f"Puntuació IMBD: {fila['score_imbd']}")
            print(f"{fila['name_type']}")
            print(f"Temporades: {fila['seasons_contingut_cinematografic']}")
            print(f"Plataformes: {fila['plataformes_disponibles']}")
            print(f"Gèneres: {fila['generes']}")
            print(f"Durada: {fila['runtime_contingut_cinematografic']} minuts")
            print(f"Any: {fila['release_year_contingut_cinematografic']}")
            print(f"Paissos: {fila['paissos']}")
            print(f"Classificació: {fila['name_any_certificacio']}")
            print(f"Descripció: {fila['description_contingut_cinematografic']}")
            print("------------------------------------------------------")
            
def obtenir_opcio(pregunta, opcions):
    while True:
        print(pregunta)
        for key, value in opcions.items():
            print(f"{key}. {value}")
        opcio = input("Selecciona una opció: ")
        if opcio.isdigit() and int(opcio) in opcions:
            return int(opcio)
        else:
            print("Opció no vàlida. Introdueix un número vàlid.")

# Funció per obtenir el filtre de gènere
def obtenir_genere():
    genere = input("Selecciona el gènere (o prem Enter per ometre-ho):\n0: war\n1: sport\n2: scifi\n3: thriller\n4: european\n5: romance\n6: documentation\n7: drama\n8: music\n8: reality\n10: horror\n11: fantasy\n12: animation\n13: comedy\n14: western\n15: family\n16: crime\n17: history\n18: action\nIntrodueix: ")
    if genere.strip():
        claus_genere = f"cg.idgenere = {genere}"
        return claus_genere
    else:
        return None

# Funció per obtenir el filtre d'any
def obtenir_any():
    any = input("Introdueix l'any (o prem Enter per ometre-ho): ")
    if any.strip():
        any_num= int(any)
        any_mes= any_num+5
        any_menos= any_num-5
        any_mes_str=str(any_mes)
        any_menos_str = str(any_menos)
        return f"cc.release_year_contingut_cinematografic <= {any_mes} AND cc.release_year_contingut_cinematografic >= {any_menos}"
    else:
        return None

def obtenir_num_temporades():
    numero = input("Introdueix el número màxim de temporades disposades a veure (o prem Enter per ometre-ho):")
    if numero.strip():
        return f"cc.seasons_contingut_cinematografic <= {numero}"
    else:
        return None

# Funció per obtenir el títol de cerca
def obtenir_titol_cerca():
    titol = input("Introdueix el títol a cercar (o prem Enter per ometre-ho): ")
    if titol.strip():
        return f"cc.title_contingut_cinematografic LIKE '{titol}%'"
    else:
        return None
    
def obtenir_durada_maxima():
    durada_max = input("Introdueix la durada màxima dessitjada en minuts (o prem Enter per ometre-ho):")
    if durada_max.strip():
        return f"cc.runtime_contingut_cinematografic <= {durada_max}"
    else:
        return None
    
def obtenir_durada_minima():
    durada_min = input("Introdueix la durada mínima dessitjada en minuts (o prem Enter per ometre-ho):")
    if durada_min.strip():
        return f"cc.runtime_contingut_cinematografic >= {durada_min}"
    else:
        return None
    
def obtenir_NO_any_certificacio():
    llista = []
    while True:
        certificat = input("Introdueix el número de l'opció (o prem Enter per ometre-ho),\n0: TV-PG\n1: PG\n2: G\n3: PG-13\n4: R\n5: TV-G\n6: TV-Y\n7: TV-14\n8: NC-17\n9: TV-Y7\n10: TV-MA\n")
        if certificat.strip():
            llista.append(certificat)
        else:
            break
    if len(llista) > 0:
        cadena_certificats = ', '.join([f"'{cert}'" for cert in llista])
        return f"cc.id_contingut_cinematografic NOT IN ({cadena_certificats})"
    else:
        return None
    
def obtenir_pais():
    pais = input("Introdueix l'abreniatura d'un país (o prem Enter per ometre-ho):")
    if pais.strip():
        return f"pa.name_paisos LIKE '{pais}%'"
    else:
        return None


# Funció per construir la consulta SQL
def construir_consulta(tipus_contingut, genere=None, any=None, titol_cerca=None, num_temp=None, durada_max=None, durada_min=None, certificat=None, pais=None):
    ordenacioPopularity_Votes = "\nGROUP BY cc.title_contingut_cinematografic\nORDER BY imbd.score_imbd DESC, imbd.votes_imbd DESC"
    consulta = f"""
        SELECT cc.title_contingut_cinematografic,imbd.score_imbd,type.name_type,cc.seasons_contingut_cinematografic,cc.runtime_contingut_cinematografic,cc.description_contingut_cinematografic,cc.release_year_contingut_cinematografic,ac.name_any_certificacio,
        GROUP_CONCAT(DISTINCT p.name_plataforma SEPARATOR ', ') AS plataformes_disponibles,
        GROUP_CONCAT(DISTINCT g.name_genere SEPARATOR ', ') AS generes,
        GROUP_CONCAT(DISTINCT pa.name_paisos SEPARATOR ', ') AS paissos
        FROM contingut_cinematografic cc
        JOIN imbd ON cc.id_imbd = imbd.idimbd 
        JOIN type ON cc.type_contingut_cinematografic = type.id_type
        JOIN contingutcinematografic_plataforma cp ON cc.id_contingut_cinematografic = cp.idcontingutCinematografic
        JOIN plataforma p ON cp.idplataforma = p.idplataforma
        JOIN contingutcinematografic_genere cg ON cc.id_contingut_cinematografic = cg.idcontingutCinematografic
        JOIN genere g ON cg.idgenere = g.idgenere
        JOIN any_certificacio ac ON cc.id_ac_contingut_cinematografic = ac.idany_certificacio
        JOIN contingutcinematografic_paisos ccp ON cc.id_contingut_cinematografic = ccp.idcontingutCinematografic
        JOIN paisos pa ON ccp.id_paisos = pa.idpaisos
        """
    if tipus_contingut:
        consulta += f"WHERE (cc.type_contingut_cinematografic = '{tipus_contingut}')"
    
    if genere:
        consulta +=f" AND {genere}"

    if any:
        consulta += f" AND {any}"
            
    if titol_cerca:
        consulta += f" AND {titol_cerca}"
    
    if num_temp:
        consulta += f" AND {num_temp}"
        
    if durada_max:
        consulta += f" AND {durada_max}"

    if durada_min:
        consulta += f" AND {durada_min}"
        
    if certificat:
        consulta += f" AND {certificat}"

    if pais:
        consulta += f" AND {pais}"
    # Agregar el ordenamiento por popularidad y votos de TMBD e IMBD
    consulta += f" {ordenacioPopularity_Votes}"
    
    return consulta




def seleccionar_tipo_contingut(opcio):
    if opcio == 1:
        return "1"
    elif opcio == 2:
        return "0" 
    elif opcio == 3:
        return "0' OR cc.type_contingut_cinematografic = '1"
    else:
        return None

# Preguntar a l'usuari si vol utilitzar filtres o cercar per títol
opcions_us_filtres = {1: "Utilitzar filtres", 2: "Cercar per títol"}
us_filtres = obtenir_opcio("Com vols cercar?", opcions_us_filtres)

# En funció de l'opció seleccionada, obtenir els filtres corresponents
numtemp = None
if us_filtres == 1:
    opcions_tipus_contingut = {1: "Sèries", 2: "Pel·lícules", 3: "Tot el contingut"}
    tipus_contingut_opcio = obtenir_opcio("Selecciona el tipus de contingut:", opcions_tipus_contingut)
    tipus_contingut = seleccionar_tipo_contingut(tipus_contingut_opcio)
    if tipus_contingut == '1':
        numtemp = obtenir_num_temporades()
    genere = obtenir_genere()
    any = obtenir_any()
    durada_max = obtenir_durada_maxima()
    durada_min = obtenir_durada_minima()
    certificat = obtenir_NO_any_certificacio()
    pais= obtenir_pais()
    titol_cerca = None
else:
    tipus_contingut = None
    genere = None
    any = None
    durada_max = None
    durada_min = None
    certificat = None
    pais = None
    titol_cerca = obtenir_titol_cerca()

# Construir i mostrar la consulta SQL final
consulta_final = construir_consulta(tipus_contingut, genere, any, titol_cerca, numtemp, durada_max, durada_min, certificat, pais)
#print("Consulta SQL final:")
#print(consulta_final)

import pymysql.cursors

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()
cursor.execute(consulta_final)
filas = cursor.fetchall()


mostrar_lote(filas, 0, 10)

indice = 10
while indice < len(filas):
    respuesta = input("Vols veure les pròximes deu recomanacions? (S/N): ")
    if respuesta.lower() == 's':
        mostrar_lote(filas, indice, indice + 10)
        indice += 10
    else:
        break
connection.close()