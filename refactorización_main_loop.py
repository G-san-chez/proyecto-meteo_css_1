from historial import reporte_cobertura_geografica, reporte_estadisticas_sesion
from consumidor_de_json import cargar_datos_caracas
from consumidor_api import obtener_clima

# Creamos la clase que exige la rúbrica para guardar el historial y evitar diccionarios
class ConsultaClima:
    """
    Clase para instanciar y almacenar los datos de cada consulta 
    realizada durante la sesión activa, cumpliendo con la regla de POO.
    """
    def __init__(self, municipio, localidad, temperatura, humedad, viento, estado_tiempo):
        self.municipio = municipio
        self.localidad = localidad
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.estado_tiempo = estado_tiempo

municipios_cargados = cargar_datos_caracas('zonas_caracas.json')

class APP_1:
    """Clase principal que gestiona el ciclo de vida de la aplicación y la interfaz en consola."""
    
    def start(self):
        """Inicia el bucle principal del menú de usuario."""
        historial_consultas = []  # Definir la lista para almacenar OBJETOS del historial
        opcion = ""
        while opcion != "5":
            print("\n=== CONSULTA DEL CLIMA ===")
            print("1. Buscar por Municipio")
            print("2. Buscar por nombre de Localidad")
            print("3. Módulo de Reportes y Estadísticas")
            print("4. Módulo de Datos Históricos (Por Período)")
            print("5. Salir")
            opcion = input("Elija una opción: ")

            # Buscar por Municipio y localidad
            if opcion == "1":
                print("\n--- LISTA DE MUNICIPIOS ---")
                contador = 1
                for mun in municipios_cargados:
                    print(str(contador) + ". " + mun.nombre)
                    contador += 1

                num_mun = int(input("Seleccione el número del municipio: ")) - 1
                municipio_elegido = municipios_cargados[num_mun]

                # Guardamos solo las localidades que SÍ tienen coordenadas
                localidades_validas = []
                for loc in municipio_elegido.lista_localidades:
                    if loc.latitud != None and loc.longitud != None:
                        localidades_validas.append(loc)

                if len(localidades_validas) == 0:
                    print("Este municipio no tiene localidades con coordenadas válidas.")
                else:
                    print("\n--- LOCALIDADES DISPONIBLES ---")
                    contador = 1
                    for loc in localidades_validas:
                        print(str(contador) + ". " + loc.nombre)
                        contador += 1

                    num_loc = int(input("Seleccione el número de la localidad: ")) - 1
                    localidad_elegida = localidades_validas[num_loc]

                    # Consultamos la API (Ahora recibe y procesa el estado_tiempo)
                    temp, hum, viento, estado_tiempo = obtener_clima(localidad_elegida.latitud, localidad_elegida.longitud)

                    # Imprimimos los resultados (Se agrega el Estado del Tiempo exigido)
                    print("\n--------------------------------")
                    print("DETALLES DEL CLIMA ACTUAL")
                    print("Municipio: " + municipio_elegido.nombre)
                    print("Localidad: " + localidad_elegida.nombre)
                    print("Coordenadas: " + str(localidad_elegida.latitud) + ", " + str(localidad_elegida.longitud))
                    print("Estado del Tiempo (Código): " + str(estado_tiempo)) 
                    print("Temperatura actual: " + str(temp) + " °C")
                    print("Humedad relativa: " + str(hum) + " %")
                    print("Velocidad del viento: " + str(viento) + " km/h")
                    print("--------------------------------")

                    # ALERTA: Corrección Crítica. Se guarda un OBJETO, NO un diccionario.
                    nueva_consulta = ConsultaClima(
                        municipio_elegido.nombre,
                        localidad_elegida.nombre,
                        temp,
                        hum,
                        viento,
                        estado_tiempo
                    )
                    historial_consultas.append(nueva_consulta)

            # Busqueda directa:
            elif opcion == "2":
                texto_busqueda = input("\nIngrese el nombre de la localidad a buscar: ").lower()

                coincidencias_loc = []
                coincidencias_mun = []

                for mun in municipios_cargados:
                    for loc in mun.lista_localidades:
                        if texto_busqueda in loc.nombre.lower():
                            if loc.latitud != None and loc.longitud != None:
                                coincidencias_loc.append(loc)
                                coincidencias_mun.append(mun.nombre)

                if len(coincidencias_loc) == 0:
                    print("No se encontraron localidades con ese nombre y coordenadas válidas.")
                else:
                    print("\n--- RESULTADOS ENCONTRADOS ---")
                    contador = 1
                    for i in range(len(coincidencias_loc)):
                        print(str(contador) + ". " + coincidencias_loc[i].nombre + " (Municipio: " + coincidencias_mun[i] + ")")
                        contador += 1

                    num_sel = int(input("Seleccione el número de la localidad: ")) - 1
                    localidad_elegida = coincidencias_loc[num_sel]
                    municipio_nombre = coincidencias_mun[num_sel]

                    # Consultamos la API
                    temp, hum, viento, estado_tiempo = obtener_clima(localidad_elegida.latitud, localidad_elegida.longitud)

                    # Imprimimos los resultados
                    print("\n--------------------------------")
                    print("DETALLES DEL CLIMA ACTUAL")
                    print("Municipio: " + municipio_nombre)
                    print("Localidad: " + localidad_elegida.nombre)
                    print("Coordenadas: " + str(localidad_elegida.latitud) + ", " + str(localidad_elegida.longitud))
                    print("Estado del Tiempo (Código): " + str(estado_tiempo))
                    print("Temperatura actual: " + str(temp) + " °C")
                    print("Humedad relativa: " + str(hum) + " %")
                    print("Velocidad del viento: " + str(viento) + " km/h")
                    print("--------------------------------")

                    # ALERTA: Corrección Crítica. Se guarda un OBJETO, NO un diccionario.
                    nueva_consulta = ConsultaClima(
                        municipio_nombre,
                        localidad_elegida.nombre,
                        temp,
                        hum,
                        viento,
                        estado_tiempo
                    )
                    historial_consultas.append(nueva_consulta)

            # historial y reportes:
            elif opcion == "3":

                print("\n--- MÓDULO DE REPORTES ---")
                print("1. Ver Estadísticas de la Sesión (Ranking y Promedio)")
                print("2. Ver Cobertura Geográfica (Localidades sin coordenadas)")
                sub_opcion = input("Seleccione una opción: ")

                #  Cruzar las funciones correctas con sus listas correspondientes
                if sub_opcion == "1":
                    # Pasa la lista de OBJETOS del historial
                    reporte_estadisticas_sesion(historial_consultas)
                    
                elif sub_opcion == "2":
                    # Pasa la lista de municipios cargados del JSON
                    reporte_cobertura_geografica(municipios_cargados)
                else:
                    print("Opción no válida.")
                    
            elif opcion == "4":
                # AQUÍ INTEGRARÁS TU MÓDULO DE HISTÓRICOS Y GRÁFICOS
                print("\nIniciando módulo de históricos... (Por desarrollar)")
                
            elif opcion == "5":
                print("¡Saliendo del programa!")
                break
            else:
                print("Opción incorrecta, intente de nuevo.")
