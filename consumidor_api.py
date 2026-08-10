#Consulta la api de Open meteo :
import requests

def obtener_clima(latitud, longitud):
    """
    Consulta la API de Open-Meteo enviando latitud y longitud.
    Retorna la temperatura, humedad, velocidad del viento y el código del estado del tiempo.
    """
    # Armamos la URL con las coordenadas que nos pasan
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current_weather=true&hourly=relative_humidity_2m"
    
    # Hacemos la petición a la API
    respuesta = requests.get(url)
    datos_clima = respuesta.json()
    
    # Extraemos los datos del diccionario temporal de la API
    temperatura = datos_clima["current_weather"]["temperature"]
    viento = datos_clima["current_weather"]["windspeed"]
    estado_tiempo = datos_clima["current_weather"]["weathercode"] # Dato obligatorio agregado
    humedad = datos_clima["hourly"]["relative_humidity_2m"][0]
    
    # Retornamos los 4 valores requeridos por el sistema
    return temperatura, humedad, viento, estado_tiempo
