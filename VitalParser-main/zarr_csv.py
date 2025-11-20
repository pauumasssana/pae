import zarr
import os

def explorar_zarr(ruta_zarr):
    # Abrimos la raíz del Zarr (puede ser una carpeta en disco)
    raiz = zarr.open(ruta_zarr, mode='r')

    # Recorrer zonas (primer nivel de carpetas)
    for zona in raiz.group_keys():
        print(f'Zona: {zona}')
        grupo_zona = raiz[zona]

        # Recorrer personas dentro de una zona
        for persona in grupo_zona.group_keys():
            print(f'  Persona: {persona}')
            grupo_persona = grupo_zona[persona]

            # Listar variables (tipos de valores y timestamps)
            for variable in grupo_persona.array_keys():
                print(f'    Variable: {variable}')
                
                # Acceder a los datos (array)
                datos = grupo_persona[variable][:]
                print(f'      Datos: {datos}')  # Puedes adaptar aquí cómo quieres manejarlos

# Uso
ruta = 'ruta/al/archivo.zarr'  # Cambia por tu ruta
explorar_zarr(ruta)