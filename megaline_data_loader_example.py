import pandas as pd
import time
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_csv(*args, **kwargs):
    """
    Data loader genérico para cargar archivos CSV con reintentos y chunking.
    """
    # Se asume que name_file se pasa por los kwargs (variables globales de Mage)
    # Por defecto cargará 'megaline_users' si no se especifica.
    name_file = kwargs.get('name_file', 'megaline_users')
    filepath = f"data_example/{name_file}.csv"
    
    # Parámetros definidos
    chunk_size = 10000 
    max_retries = 3
    retry_delay = 5 

    for attempt in range(max_retries):
        try:
            chunks = []
            # Implementación de Chunking: lee el archivo en fragmentos
            for chunk in pd.read_csv(filepath, chunksize=chunk_size):
                # Aquí podrías aplicar limpieza por chunk si la RAM fuera muy limitada
                chunks.append(chunk)
            
            # Unir todos los fragmentos en un solo DataFrame
            df = pd.concat(chunks, ignore_index=True)
            print(f"Archivo {filepath} cargado exitosamente en el intento {attempt + 1}")
            return df
            
        except Exception as e:
            print(f"Error cargando {filepath} en el intento {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print(f"Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Fallo definitivo al cargar {filepath} tras {max_retries} intentos.")
