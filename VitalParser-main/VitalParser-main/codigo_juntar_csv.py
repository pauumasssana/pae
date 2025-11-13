import pandas as pd
import glob
import os

# Directorio donde están los archivos csv
directory = './CSV'  # Cambiar si es necesario

file_list = glob.glob(os.path.join(directory, '*.csv'))

merged_df = None
for file in file_list:
    col_name = os.path.basename(file).replace('.csv', '')
    df = pd.read_csv(file)
    second_col = df.columns[1]
    df = df.rename(columns={second_col: col_name})
    if merged_df is None:
        merged_df = df
    else:
        # merge_asof une tomando el valor más cercano hacia atrás (valor previo más reciente)
        merged_df = pd.merge_asof(merged_df, df, on='time', direction='backward')

if merged_df is not None:
    merged_df.to_csv('resultado_algoritmos.csv', index=False)
else:
    print("No se encontraron archivos CSV para procesar.")
