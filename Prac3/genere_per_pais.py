import folium
from folium.plugins import MarkerCluster
import json
import pandas as pd

# Archivo GeoJSON
fitxer = 'updated_countries_genere.geojson'
# Archivo CSV con coordenadas de capitales
csv_file = 'fitxersInfo/capitals.csv'

# Cargar el archivo GeoJSON
with open(fitxer, 'r') as f:
    data = json.load(f)

# Cargar el archivo CSV
capitals_df = pd.read_csv(csv_file, delimiter=';')

# Filtrar filas con coordenadas no válidas
capitals_df = capitals_df.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Crear un diccionario de coordenadas de capitales
capitales = {}
for index, row in capitals_df.iterrows():
    country = row['COUNTRY']
    lat = row['LATITUDE']
    lon = row['LONGITUDE']
    capitales[country] = {'lat': lat, 'lon': lon}

def get_color(genere):
    return {
        'documentation': '#800026',
        'war': '#BD0026',
        'sport': '#E31A1C',
        'scifi': '#FC4E2A',
        'thriller': '#FD8D3C',
        'european': '#00913f',
        'romance': '#ee6900',
        'drama': '#0d0800',
        'music': '#D4EE00',
        'reality': '#A3EE00',
        'horror': '#6C00EE',
        'fantasy': '#0000EE',
        'animation': '#00EEEE',
        'comedy': '#00EE76',
        'western': '#EE7600',
        'family': '#EE00D4',
        'crime': '#7600EE',
        'history': '#EE0076',
        'action': '#EE0000'
    }.get(genere, '#FFFFFF')

# Crear el mapa
m = folium.Map(location=[0, 0], zoom_start=2)

# Añadir capa de OpenStreetMap
folium.TileLayer('openstreetmap').add_to(m)

# Crear un cluster de marcadores
mark = MarkerCluster().add_to(m)

# Añadir marcadores para cada país en el GeoJSON
for feature in data['features']:
    properties = feature['properties']
    geometry = feature['geometry']
    
    # Obtener las coordenadas del centro del país (primer punto del polígono)
    if geometry['type'] == 'Polygon':
        coordinates = geometry['coordinates'][0][0]
    elif geometry['type'] == 'MultiPolygon':
        coordinates = geometry['coordinates'][0][0][0]

    latGeo, lonGeo = coordinates[1], coordinates[0]
    
    # Extraer propiedades
    admin = properties.get('ADMIN')
    genere = properties.get('genere')
    count_genere = properties.get('count_genere', 0)  # Proporcionar valor predeterminado 0 si es None

    # Obtener las coordenadas de la capital
    capital = capitales.get(admin)
    if capital:
        lat, lon = capital['lat'], capital['lon']
        # Usar coordenadas de la capital o del centro del país si la capital es NaN
        if not (pd.notna(lat) and pd.notna(lon)):
            lat, lon = latGeo, lonGeo
    else:
        # Si no hay capital, usar las coordenadas del centro del país
        lat, lon = latGeo, lonGeo

    # Verificar si count_genere es un número
    if isinstance(count_genere, (int, float)):
        radius = 5 + count_genere
    else:
        radius = 5  # Valor predeterminado si count_genere no es un número

    color = get_color(genere)

    # Añadir marcador circular
    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,  # Radio basado en count_genere
        popup=f'{admin}<br>Género: {genere}<br>Cantidad: {count_genere}',
        color=color,
        fill=True,
        fill_color=color
    ).add_to(mark)

# Guardar el mapa en un archivo HTML
m.save('mapa_mundo.html')
