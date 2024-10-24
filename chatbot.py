import json
import random

class SimpleAIBot:
    def __init__(self, intents_file, routes_file):
        self.intents = self.load_training_data(intents_file)
        self.routes = self.load_routes_data(routes_file)
        self.current_route = None
        self.current_destination = None
        
    def load_training_data(self, intents_file):
        with open(intents_file, 'r') as file:
            return json.load(file)['intents']
    
    def load_routes_data(self, routes_file):
        with open(routes_file, 'r') as file:
            return json.load(file)
    
    def get_route(self):
        # Preguntar al usuario por la ruta
        print("Bot: Por favor ingresa la ruta que necesitas. Ejemplo: MONTERIA-CAUCASIA BUS")
        route = input("Tú: ").upper()
        
        if route in self.routes:
            self.current_route = route
            return f"Bot: Has seleccionado la ruta {route}. Ahora, por favor ingresa el destino. Ejemplo: PL KILOMETRO 15"
        else:
            return "Bot: Lo siento, no encontré esa ruta. Por favor intenta de nuevo."
    
    def get_destination(self):
        # Preguntar al usuario por el destino una vez que la ruta esté seleccionada
        print("Bot: Por favor ingresa el destino:")
        destination = input("Tú: ").upper()
        
        available_destinations = [d['destination'] for d in self.routes[self.current_route]]
        
        if destination in available_destinations:
            self.current_destination = destination
            return self.get_fare()
        else:
            return "Bot: Lo siento, no encontré ese destino. Intenta de nuevo."
    
    def get_fare(self):
        # Buscar la tarifa basada en la ruta y destino seleccionados
        for entry in self.routes[self.current_route]:
            if entry['destination'] == self.current_destination:
                return f"Bot: El valor del pasaje de {self.current_route} a {self.current_destination} en {entry['vehicle']} es {entry['fare']}."
    
    def chat(self):
        # Flujo de conversación
        print("WhatsApp AI Bot (Presiona Ctrl+C para salir)")
        print("Bot: ¡Hola! ¿Cómo te puedo ayudar hoy?")
        
        try:
            while True:
                if not self.current_route:
                    response = self.get_route()
                    print(response)
                elif not self.current_destination:
                    response = self.get_destination()
                    print(response)
                
                if self.current_route and self.current_destination:
                    break
                    
        except KeyboardInterrupt:
            print("\nBot: ¡Adiós!")

def main():
    bot = SimpleAIBot('chatbot_intents.json', 'routes_destinations.json')  
    bot.chat()

if __name__ == "__main__":
    main()
