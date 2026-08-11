import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class RegistroHistorico:
   """
    Almacena los datos climáticos de un momento específico en el pasado.
    """
    def __init__(self, fecha, temperatura, humedad, precipitacion, viento):
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.viento = viento

def solicitar_fechas_usuario():
    """
    Maneja la entrada del usuario asegurando el formato correcto (AAAA-MM-DD).
    Aporta a la Usabilidad y Tolerancia a fallos del sistema.
    """
    while True:
        try:
            print("\n--- RANGO DE TIEMPO PARA ANÁLISIS ---")
            inicio = input("Ingrese la fecha de INICIO (AAAA-MM-DD): ")
            fin = input("Ingrese la fecha de FIN (AAAA-MM-DD): ")
            
            # Validamos que el formato sea estrictamente el solicitado
            datetime.strptime(inicio, "%Y-%m-%d")
            datetime.strptime(fin, "%Y-%m-%d")
            
            if inicio > fin:
                print("Error: La fecha de inicio no puede ser mayor que la fecha de fin.")
                continue
                
            return inicio, fin
        except ValueError:
            print("Formato incorrecto. Por favor, utilice guiones y el formato AAAA-MM-DD.")

def obtener_datos_historicos(latitud, longitud, fecha_inicio, fecha_fin):
    """
    Se conecta a la API histórica de Open-Meteo, extrae la información horaria
    y la encapsula en una lista de objetos RegistroHistorico.
    """
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitud}&longitude={longitud}&start_date={fecha_inicio}&end_date={fecha_fin}&hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
    
    lista_registros = []
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status() # Lanza error si la API rechaza la conexión
        datos = respuesta.json()
        
        tiempos = datos['hourly']['time']
        temps = datos['hourly']['temperature_2m']
        hums = datos['hourly']['relative_humidity_2m']
        precips = datos['hourly']['precipitation']
        vientos = datos['hourly']['wind_speed_10m']
        
        # Transformación obligatoria de JSON a Objetos
        for i in range(len(tiempos)):
            # Protegemos contra posibles valores nulos ('null') de la API
            t = temps[i] if temps[i] is not None else 0
            h = hums[i] if hums[i] is not None else 0
            p = precips[i] if precips[i] is not None else 0
            v = vientos[i] if vientos[i] is not None else 0
            
            registro = RegistroHistorico(tiempos[i], t, h, p, v)
            lista_registros.append(registro)
            
        return lista_registros
        
    except requests.exceptions.RequestException:
        print("\n[!] Error de conexión: No se pudo acceder al historial de Open-Meteo.")
        return []

def procesar_y_graficar_historicos(lista_registros, nombre_localidad):
    """
    Recibe la lista de objetos, utiliza Pandas para calcular promedios,
    ubicar extremos anuales y genera un gráfico comparativo con Matplotlib.
    """
    if not lista_registros:
        return

    # Extraemos los datos de los objetos para armar nuestra tabla analítica
    datos_crudos = [{
        'Fecha': r.fecha, 
        'Temp': r.temperatura, 
        'Hum': r.humedad, 
        'Precip': r.precipitacion, 
        'Viento': r.viento
    } for r in lista_registros]
    
    df = pd.DataFrame(datos_crudos)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Año'] = df['Fecha'].dt.year
    df['Mes'] = df['Fecha'].dt.month

    # 4.a: Cálculos agrupados por mes y año
    resumen_mensual = df.groupby(['Año', 'Mes']).agg({
        'Temp': 'mean',
        'Hum': 'mean',
        'Precip': 'sum',
        'Viento': 'mean'
    }).reset_index()

    print(f"\n=== HISTÓRICO MENSUAL: {nombre_localidad.upper()} ===")
    for _, fila in resumen_mensual.iterrows():
        print(f"Año {int(fila['Año'])}, Mes {int(fila['Mes']):02d} | "
          f"Temp: {fila['Temp']:.1f}°C | Humedad: {fila['Hum']:.0f}% | "
          f"Lluvia: {fila['Precip']:.1f}mm | Viento: {fila['Viento']:.1f}km/h")

    # 4.b: Promedios generales del período
    print("\n--- PROMEDIOS TOTALES DEL PERÍODO ---")
    print(f"Temperatura media: {df['Temp'].mean():.2f} °C")
    print(f"Humedad relativa media: {df['Hum'].mean():.2f} %")
    print(f"Precipitación total acumulada: {df['Precip'].sum():.2f} mm")
    print(f"Velocidad media del viento: {df['Viento'].mean():.2f} km/h")

    # 4.c: Años Extremos
    resumen_anual = df.groupby('Año').agg({
        'Temp': 'mean',
        'Hum': 'mean',
        'Precip': 'sum'
    })
    
    print("\n--- ANÁLISIS DE EXTREMOS ANUALES ---")
    # idxmax() nos da el índice (en este caso el Año) donde ocurrió el valor máximo/mínimo
    print(f"Año más caluroso: {resumen_anual['Temp'].idxmax()}")
    print(f"Año más fresco: {resumen_anual['Temp'].idxmin()}")
    print(f"Año con mayor precipitación: {resumen_anual['Precip'].idxmax()}")
    print(f"Año con mayor humedad relativa: {resumen_anual['Hum'].idxmax()}")

    # 4.d: Gráfico Comparativo
    print("\nGenerando gráfico comparativo. Por favor, revise la nueva ventana...")
    
    figura, ejes = plt.subplots(2, 2, figsize=(12, 8))
    figura.suptitle(f"Evolución Climática Anual - {nombre_localidad}", fontsize=14, fontweight='bold')

    # Configuración de los 4 subgráficos con colores distintivos
    ejes[0, 0].plot(resumen_anual.index, resumen_anual['Temp'], marker='o', color='crimson')
    ejes[0, 0].set_title('Temperatura Media Anual (°C)')
    ejes[0, 0].set_xticks(resumen_anual.index)

    ejes[0, 1].plot(resumen_anual.index, resumen_anual['Hum'], marker='s', color='teal')
    ejes[0, 1].set_title('Humedad Relativa Media Anual (%)')
    ejes[0, 1].set_xticks(resumen_anual.index)

    ejes[1, 0].bar(resumen_anual.index, resumen_anual['Precip'], color='steelblue')
    ejes[1, 0].set_title('Precipitación Total Anual (mm)')
    ejes[1, 0].set_xticks(resumen_anual.index)

    # Viento medio por año
    viento_anual = df.groupby('Año')['Viento'].mean()
    ejes[1, 1].plot(viento_anual.index, viento_anual.values, marker='^', color='darkorange', linestyle='--')
    ejes[1, 1].set_title('Velocidad Media del Viento Anual (km/h)')
    ejes[1, 1].set_xticks(viento_anual.index)

    plt.tight_layout()
    plt.show()
