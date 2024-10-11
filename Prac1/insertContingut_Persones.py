import pandas as pd
import pymysql.cursors

# Conectarse a la base de datos
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sio_1',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()

# Leer el archivo CSV con la información de las personas
persones1 = pd.read_csv('Prac1/persones.csv')
persones = persones1.drop_duplicates()
# Consulta SQL para insertar los datos en la tabla
consulta_insertar = "INSERT INTO contingutcinematografic_persones (id_persona, id_contingutCinematografic, id_rols, name_character) VALUES (%s,%s,%s,%s)"

# Consulta SQL para verificar si una película está en la base de datos
consulta_pelicula_en_bd = "SELECT * FROM contingut_cinematografic WHERE id_contingut_cinematografic = %s"

# Recorrer el DataFrame de personas
for indice, fila in persones.iterrows():
    try:
        # Verificar si la fila contiene un ID válido
        if not pd.isna(fila['id']):
            cursor.execute(consulta_pelicula_en_bd, (fila['id'],))
            resultado = cursor.fetchone()
            # Si no hay resultado, la película no está en la base de datos, saltar a la próxima iteración
            if not resultado:
                continue
        else:
            continue
        
        # Saltar si el rol o el ID de la persona están vacíos
        if pd.isna(fila['role']) or pd.isna(fila['person_id']):
            continue
        
        # Asignar el valor correcto según el rol
        if fila['role'] == "DIRECTOR":
            valor = (fila['person_id'], fila['id'], str(1), "DIRECTOR")
        elif fila['role'] == "ACTOR":
            if fila['character']:
                valor = (fila['person_id'], fila['id'], str(0), str(fila['character']))
            else:
                valor = (fila['person_id'], fila['id'], str(0), "UNKNOWN CHARACTER")
        else:
            continue
        
        # Ejecutar la consulta SQL para insertar los datos en la tabla
        cursor.execute(consulta_insertar, valor)
        
            
    except pymysql.err.IntegrityError as e:
        print(f"Error de integridad: {e}")
        continue

# Confirmar los cambios en la base de datos
connection.commit()

# Cerrar el cursor y la conexión
cursor.close()
connection.close()
