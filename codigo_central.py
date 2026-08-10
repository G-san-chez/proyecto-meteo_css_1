from historial import reporte_cobertura_geografica, reporte_estadisticas_sesion
from consumidor_de_json import cargar_datos_caracas,generar_reporte_caracas
from consumidor_api import obtener_clima
from modulo_historicos import solicitar_fechas_usuario, obtener_datos_historicos, procesar_y_graficar_historicos
municipios_cargados = cargar_datos_caracas('zonas_caracas.json')
class APP_1:
 
   
    

# MENÚ PRINCIPAL para busquedas:

    def start (self):
        
     historial_consultas = []#Definir la lista para el historial antes del bucle
     generar_reporte_caracas(municipios_cargados)  
        opcion = ""
        while opcion != "5":
            print("\n=== CONSULTA DEL CLIMA ===")
            print("1. Buscar por Municipio")
            print("2. Buscar por nombre de Localidad")
            print("3. Módulo de Reportes")
            print("4. modulo de datos historicos")
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

                    # Consultamos la API
                    temp, hum, viento, estado_tiempo = obtener_clima(localidad_elegida.latitud, localidad_elegida.longitud)

                    # Imprimimos los resultados
                    print("\n--------------------------------")
                    print("DETALLES DEL CLIMA")
                    print("Municipio: " + municipio_elegido.nombre)
                    print("Localidad: " + localidad_elegida.nombre)
                    print("Coordenadas: " + str(localidad_elegida.latitud) + ", " + str(localidad_elegida.longitud))
                    print("Temperatura actual: " + str(temp) + " °C")
                    print("Humedad relativa: " + str(hum) + " %")
                    print("Velocidad del viento: " + str(viento) + " km/h")
                    print("--------------------------------")

                    # Guardar en el historial de consultas
                    consulta_realizada = {
                        'municipio': municipio_elegido.nombre,
                        'localidad': localidad_elegida.nombre,
                        'temperatura': temp
                    }
                    historial_consultas.append(consulta_realizada)

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
                    print("DETALLES DEL CLIMA")
                    print("Municipio: " + municipio_nombre)
                    print("Localidad: " + localidad_elegida.nombre)
                    print("Coordenadas: " + str(localidad_elegida.latitud) + ", " + str(localidad_elegida.longitud))
                    print("Temperatura actual: " + str(temp) + " °C")
                    print("Humedad relativa: " + str(hum) + " %")
                    print("Velocidad del viento: " + str(viento) + " km/h")
                    print("--------------------------------")

                    # Guardar en el historial de consultas
                    consulta_realizada = {
                        'municipio': municipio_nombre,
                        'localidad': localidad_elegida.nombre,
                        'temperatura': temp
                    }
                    historial_consultas.append(consulta_realizada)

            # historial y reportes:
            elif opcion == "3":

                print("\n--- MÓDULO DE REPORTES ---")
                print("1. Ver Estadísticas de la Sesión (Ranking y Promedio)")
                print("2. Ver Cobertura Geográfica (Localidades sin coordenadas)")
                sub_opcion = input("Seleccione una opción: ")

                #  Cruzar las funciones correctas con sus listas correspondientes
                if sub_opcion == "1":
                    # Pasa la lista del historial
                    reporte_estadisticas_sesion(historial_consultas)
                    
                elif sub_opcion == "2":
                    # Pasa la lista de municipios cargados del JSON
                    reporte_cobertura_geografica(municipios_cargados)
                else:
                    print("Opción no válida.")

            elif opcion == "4":
                print("\n--- MÓDULO DE DATOS HISTÓRICOS ---")
                
                # Primero, pedimos seleccionar la localidad mediante búsqueda directa
                texto = input("Ingrese el nombre de la localidad a evaluar: ").lower()
                coincidencias = []
                
                for mun in municipios_cargados:
                    for loc in mun.lista_localidades:
                        if texto in loc.nombre.lower() and loc.latitud is not None:
                            coincidencias.append(loc)
                            
                if len(coincidencias) == 0:
                    print("No se encontraron localidades con ese nombre y coordenadas válidas.")
                else:
                    contador = 1
                    for c in coincidencias:
                        print(f"{contador}. {c.nombre}")
                        contador += 1
                        
                    num_sel = int(input("Seleccione el número de la localidad: ")) - 1
                    loc_hist = coincidencias[num_sel]
                    
                    # Pedimos fechas, consultamos API y procesamos
                    fecha_ini, fecha_fin = solicitar_fechas_usuario()
                    lista_historica = obtener_datos_historicos(loc_hist.latitud, loc_hist.longitud, fecha_ini, fecha_fin)
                    
                    if lista_historica:
                        procesar_y_graficar_historicos(lista_historica, loc_hist.nombre)
                        
            elif opcion == "5":
                print("¡Saliendo del programa!")
                break
                
            else:
                print("Opción incorrecta, intente de nuevo.")                
