import pandas as pd
import json

# Cargar el archivo Excel
file_path = 'TARIFAS_SEP_2024.xlsx'  # Asegúrate de tener este archivo en el mismo directorio
sheet_name = 'tarifas'  # Cambia si la hoja tiene otro nombre
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Lista para almacenar los intents
intents = []
routes = {}

# Iterar a través de las filas del archivo Excel para generar intents y un diccionario de rutas y destinos
for index, row in data.iterrows():
    route = row['RUTA']
    destination = row['DESTINO']
    vehicle = row['CLASE VEHICULO']
    fare = row['VALOR PASAJE']

    # Crear intents para cada ruta y destino
    intent = {
        "tag": f"{route} - {destination}",
        "patterns": [
            f"¿Cuál es la tarifa de {route} a {destination} en {vehicle}?",
            f"¿Cuánto cuesta el pasaje de {route} a {destination} en {vehicle}?",
            f"¿Cuál es el costo de viajar de {route} a {destination} en {vehicle}?"
        ],
        "responses": [
            f"El valor del pasaje de {route} a {destination} en {vehicle} es {fare}."
        ]
    }
    intents.append(intent)

    # Guardar las rutas y sus destinos
    if route not in routes:
        routes[route] = []
    routes[route].append({
        "destination": destination,
        "vehicle": vehicle,
        "fare": fare
    })

# Guardar los intents en un archivo JSON
output_file = 'chatbot_intents.json'
with open(output_file, 'w') as file:
    json.dump({"intents": intents}, file, indent=4)

print(f"Archivo JSON generado correctamente: {output_file}")

# Guardar las rutas y destinos en otro archivo JSON
routes_file = 'routes_destinations.json'
with open(routes_file, 'w') as file:
    json.dump(routes, file, indent=4)

print(f"Archivo de rutas y destinos generado correctamente: {routes_file}")
