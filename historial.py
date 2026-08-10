

def reporte_cobertura_geografica(municipios_cargados):
    print()
    print("COBERTURA GEOGRÁFICA - LOCALIDADES SIN COORDENADAS")
    print()

    total_sin_coords = 0

    # Recorremos cada municipio de la lista
    for mun in municipios_cargados:
        print("\nMunicipio: " + mun.nombre)
        
        contador_mun_sin_coords = 0
        
        # Recorremos las localidades de este municipio
        for loc in mun.lista_localidades:
            # Revisamos si no tiene coordenadas
            if loc.latitud == None or loc.longitud == None:
                # Usamos loc.localidad o loc.nombre de forma normal
                print("  * " + str(loc.nombre))
                
                contador_mun_sin_coords = contador_mun_sin_coords + 1
                total_sin_coords = total_sin_coords + 1
        
        # Si el municipio no tuvo ninguna localidad sin coordenadas
        if contador_mun_sin_coords == 0:
            print("  (Todas las localidades tienen coordenadas)")

    print()
    print("Total global de localidades sin coordenadas: " + str(total_sin_coords))
    print()


def reporte_estadisticas_sesion(historial_consultas):
    print()
    print("ESTADÍSTICAS Y RANKING DE LA SESIÓN ACTIVA")
    print()

    # Si la lista de consultas está vacía
    if len(historial_consultas) == 0:
        print("\nNo se han realizado consultas de clima en esta sesión.")
        print("Realice alguna búsqueda para generar estadísticas.")
        print()
        return

    # Variables para encontrar la más cálida y la más fría
    # Las inicializamos con el primer elemento del historial
    mas_calida = historial_consultas[0]
    mas_fria = historial_consultas[0]
    
    suma_temperaturas = 0

    # Recorremos las consultas guardadas una por una
    for consulta in historial_consultas:
        temp_actual = consulta['temperatura']
        
        # Acumulamos la temperatura para el promedio
        suma_temperaturas = suma_temperaturas + temp_actual

        # Comprobamos si esta temperatura es mayor que la más cálida registrada hasta ahora
        if temp_actual > mas_calida['temperatura']:
            mas_calida = consulta

        # Comprobamos si esta temperatura es menor que la más fría registrada hasta ahora
        if temp_actual < mas_fria['temperatura']:
            mas_fria = consulta

    # Calculamos el promedio manualmente
    total_consultas = len(historial_consultas)
    promedio = suma_temperaturas / total_consultas

    # Mostramos los resultados
    print("\n1. RANKING DE TEMPERATURAS")
    print("Localidad más cálida:")
    print("  - Municipio: " + mas_calida['municipio'])
    print("  - Localidad: " + mas_calida['localidad'])
    print("  - Temperatura: " + str(mas_calida['temperatura']) + " °C")

    print("\nLocalidad más fría:")
    print("  - Municipio: " + mas_fria['municipio'])
    print("  - Localidad: " + mas_fria['localidad'])
    print("  - Temperatura: " + str(mas_fria['temperatura']) + " °C")

    print("\n2. PROMEDIO GENERAL DE LA SESIÓN")
    print("  - Total de consultas realizadas: " + str(total_consultas))
    print("  - Promedio de temperatura: " + str(round(promedio, 2)) + " °C")
    print()