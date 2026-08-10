import json
from localidad_y_municipio import Localidad, Municipio


def cargar_datos_caracas(ruta_archivo='zonas_caracas.json'):
    """Carga el JSON de zonas de Caracas y devuelve una lista de objetos Municipio."""
    municipios_cargados = []

    # 'with' cierra el archivo automáticamente al terminar
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    for nombre_mun, localidades_json in datos.items():
        nuevo_municipio = Municipio(nombre_mun)

        for item_loc in localidades_json:
            nueva_localidad = Localidad(
                item_loc.get('localidad'),
                item_loc.get('latitud'),
                item_loc.get('longitud')
            )
            nuevo_municipio.agregar_localidad(nueva_localidad)

        #un append por cada municipio
        municipios_cargados.append(nuevo_municipio)

    return municipios_cargados


def generar_reporte_caracas(municipios):
    """Recibe la lista de municipios e imprime el reporte estadístico en consola."""
    print("\tREPORTE DE CARGA DE DATOS - ZONAS DE CARACAS")
    print("=" * 60)

    total_global_cargadas = 0
    total_global_con_coords = 0

    for mun in municipios:
        cargadas = 0
        con_coords = 0
        sin_coords = 0

        for loc in mun.lista_localidades:
            cargadas += 1
            if loc.latitud is not None and loc.longitud is not None:
                con_coords += 1
            else:
                sin_coords += 1

        porcentaje = (con_coords / cargadas * 100) if cargadas > 0 else 0.0

        total_global_cargadas += cargadas
        total_global_con_coords += con_coords

        print(f"Municipio: {mun.nombre}")
        print(f"  - Localidades cargadas: {cargadas}")
        print(f"  - Con coordenadas: {con_coords}")
        print(f"  - Sin coordenadas: {sin_coords}")
        print(f"  - Porcentaje con coords: {round(porcentaje, 2)}%\n")

    # Resumen general
    total_global_sin_coords = total_global_cargadas - total_global_con_coords
    pct_global = (total_global_con_coords / total_global_cargadas * 100) if total_global_cargadas > 0 else 0.0

    print("=" * 60)
    print("TOTALES GENERALES (CARACAS)")
    print(f"Total localidades cargadas: {total_global_cargadas}")
    print(f"Total con coordenadas: {total_global_con_coords}")
    print(f"Total sin coordenadas: {total_global_sin_coords}")
    print(f"Porcentaje total con coords: {round(pct_global, 2)}%")


