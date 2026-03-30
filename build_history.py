import os
import json
import re

def consolidar_historial():
    data_historica = []
    patron_fecha = re.compile(r'^(\d{4}-\d{2}-\d{2})')
    directorio = 'data_trello' # Apuntamos a tu carpeta
    
    print("📂 Escaneando historial de Trello...")
    archivos = [f for f in os.listdir(directorio) if f.endswith('.json')]
    archivos.sort() 

    for nombre_archivo in archivos:
        match = patron_fecha.match(nombre_archivo)
        if match:
            fecha = match.group(1)
            ruta_completa = os.path.join(directorio, nombre_archivo)
            try:
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    contenido = json.load(f)
                    data_historica.append({
                        "fecha": fecha,
                        "archivo": nombre_archivo,
                        "data": contenido
                    })
            except Exception as e:
                print(f"❌ Error leyendo {nombre_archivo}: {e}")
                
    # Escribir el gran paquete JSON en la raíz
    with open('history_all.json', 'w', encoding='utf-8') as f:
        json.dump(data_historica, f)
        
    print(f"✅ history_all.json generado con éxito con {len(data_historica)} registros.")

if __name__ == "__main__":
    consolidar_historial()
