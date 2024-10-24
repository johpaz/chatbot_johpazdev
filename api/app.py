from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta principal
@app.route('/')
def home():
    return "¡Hola, mundo desde Flask!"

# Crear una ruta para recibir datos desde un POST
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # Procesa los datos como quieras
    return jsonify({"message": "Datos recibidos", "data": data})

if __name__ == '__main__':
    app.run(debug=True)
