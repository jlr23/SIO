import json
import Levenshtein

# Leer el archivo JSON existente
with open('fitxersDadesAnalisi/num_series_y_peliculas_por_pais.json', 'r') as file:
    data = json.load(file)

# Leer el archivo GeoJSON
with open('fitxersInfo/countries.geojson', 'r') as file:
    geojson_data = json.load(file)

# Extraer los códigos de tres letras del GeoJSON
geojson_country_codes = [feature['properties']['ISO_A3'] for feature in geojson_data['features']]

# Función para encontrar la mejor coincidencia de código
def find_best_match(code, options):
    best_match = None
    best_distance = float('inf')
    for option in options:
        distance = Levenshtein.distance(code, option)
        if distance < best_distance:
            best_distance = distance
            best_match = option
    return best_match

# Transformar la estructura de datos
structured_data = {}
for country_code, values in data.items():

    

    num_series = values['num_series']
    num_peliculas = values['num_peliculas']
    

    best_match = find_best_match(country_code, geojson_country_codes)
    if best_match:
        structured_data[best_match] = {
            "num_series": num_series,
            "num_peliculas": num_peliculas
        }
# Actualizar el archivo GeoJSON con los datos estructurados
for feature in geojson_data['features']:
    country_code = feature['properties']['ISO_A3']
    if country_code in structured_data:
        feature['properties'].update(structured_data[country_code])

# Guardar el archivo GeoJSON actualizado
with open('updated_countries_series_pelis.geojson', 'w') as file:
    json.dump(geojson_data, file, indent=4, ensure_ascii=False)

print("GeoJSON actualizado y guardado en 'updated_countries_genere.geojson'")
