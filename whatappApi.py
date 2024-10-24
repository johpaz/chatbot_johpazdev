import requests
import json

# Datos de autenticación y configuración
API_URL = 'https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages'  # Cambia el número de teléfono y versión de API
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'  # El token que te da Meta para la API de WhatsApp

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def send_list_message(to_number):
    """
    Envía un mensaje interactivo tipo lista (List Messages) con opciones de rutas.
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Selecciona tu ruta"
            },
            "body": {
                "text": "Por favor, elige una ruta para continuar."
            },
            "action": {
                "button": "Ver rutas",
                "sections": [
                    {
                        "title": "Rutas disponibles",
                        "rows": [
                            {
                                "id": "route_1",
                                "title": "MONTERIA-CAUCASIA BUS",
                                "description": "Ruta a Caucasia"
                            },
                            {
                                "id": "route_2",
                                "title": "MONTERIA-PLANETA RICA",
                                "description": "Ruta a Planeta Rica"
                            }
                        ]
                    }
                ]
            }
        }
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Mensaje enviado correctamente.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def send_reply_buttons(to_number, route):
    """
    Envía botones de respuesta rápida (Reply Buttons) con destinos disponibles según la ruta seleccionada.
    """
    destinations = {
        "MONTERIA-CAUCASIA BUS": [
            {"id": "destination_1", "title": "PL KILOMETRO 15"},
            {"id": "destination_2", "title": "PL PATIO BONITO"}
        ],
        "MONTERIA-PLANETA RICA": [
            {"id": "destination_3", "title": "CENTRAL PLANETA RICA"},
            {"id": "destination_4", "title": "PL MONTERIA TERMINAL"}
        ]
    }

    buttons = [
        {"type": "reply", "reply": {"id": destination['id'], "title": destination['title']}}
        for destination in destinations.get(route, [])
    ]

    if buttons:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {
                    "type": "text",
                    "text": f"Destinos para {route}"
                },
                "body": {
                    "text": "Por favor, selecciona un destino:"
                },
                "action": {
                    "buttons": buttons
                }
            }
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Mensaje enviado correctamente.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    else:
        print("No se encontraron destinos para la ruta seleccionada.")

def send_fare_message(to_number, route, destination):
    """
    Envía el valor del pasaje para la ruta y destino seleccionados.
    """
    fares = {
        "MONTERIA-CAUCASIA BUS": {
            "PL KILOMETRO 15": 6000,
            "PL PATIO BONITO": 9000
        },
        "MONTERIA-PLANETA RICA": {
            "CENTRAL PLANETA RICA": 10000,
            "PL MONTERIA TERMINAL": 8000
        }
    }

    fare = fares.get(route, {}).get(destination, "No disponible")

    if fare != "No disponible":
        message = f"El valor del pasaje de {route} a {destination} es {fare}."
    else:
        message = "Lo siento, no tenemos información sobre esa ruta y destino."

    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Mensaje enviado correctamente.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Ejemplo de uso
user_number = "whatsapp:+123456789"  # Reemplaza con el número de WhatsApp del usuario

# 1. Enviar lista de rutas
send_list_message(user_number)

# 2. Supongamos que el usuario selecciona "MONTERIA-CAUCASIA BUS"
selected_route = "MONTERIA-CAUCASIA BUS"

# 3. Enviar botones con destinos para esa ruta
send_reply_buttons(user_number, selected_route)

# 4. Supongamos que el usuario selecciona "PL KILOMETRO 15"
selected_destination = "PL KILOMETRO 15"

# 5. Enviar el valor del pasaje
send_fare_message(user_number, selected_route, selected_destination)
