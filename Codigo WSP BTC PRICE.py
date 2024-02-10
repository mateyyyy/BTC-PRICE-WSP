from flask import Flask, request
import ccxt
from heyoo import WhatsApp

app = Flask(__name__)

def obtener_precio_bitcoin():
    # Crear una instancia del intercambio de Binance
    exchange = ccxt.binance()

    # Obtener el ticker del par BTC/USDT (Bitcoin en dólares estadounidenses)
    ticker = exchange.fetch_ticker('BTC/USDT')

    # Obtener el precio del último intercambio
    precio = ticker['last']

    return precio

def enviar():
    # **Reemplaza estos valores con los tuyos**
    token = "EAAMk2yjrUI4BO3L8kzBEHJJpi0OplT2vFqOICHxEpKS0Nqw0q4tljcykyxrFzOybYVsNcxF7i26Vp9yg8P2ZChbkEQIjpJZBwB1fgCgJZCZCYjYhvTH0lOxCxZBFpR4ZB0cHxUWHn8iGbPH3DLD1HFmm6x09Xte5Fr03GVD0mbfrg27BcZAoOvaC7Rfnar5B1Vc0NiYHP9tODDlZCHP4uyAZD"
    idNumeroTelefono = "108720192163176"
    telefonoEnvia = "542657541156"
    precio_bitcoin = obtener_precio_bitcoin()
    textoMensaje = f"Precio del Bitcoin en USD: {precio_bitcoin}"
    mensajeWa = WhatsApp(token, idNumeroTelefono)
    mensajeWa.send_message(textoMensaje, telefonoEnvia)

    return "Mensaje enviado exitosamente"

@app.route("/webhook", methods=["POST"])
def recibirMsg():
    if request.method == "GET":
        # SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "HolaNovato":
            # ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            return "Error de autentificacion."
    elif request.method == "POST":
        data = request.get_json()
        mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        if(mensaje=='BTC'):
            enviar()
        with open("texto.txt", "w") as f:
            f.write(str(mensaje))
        return "Mensaje recibido y guardado exitosamente"

if __name__ == "__main__":
    app.run()

