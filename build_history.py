import os
import json
import re

def consolidar_historial():
    data_historica = []
    patron_fecha = re.compile(r'^(\d{4}-\d{2}-\d{2})')
    directorio = 'data_trello' 
    
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
                    
                    # --- OPTIMIZACIÓN EXTREMA DE TAMAÑO ---
                    # Extraemos SOLO lo que el index.html necesita para funcionar.
                    
                    listas_opt = [{"id": l["id"], "name": l["name"], "closed": l.get("closed", False)} for l in contenido.get("lists", [])]
                    
                    labels_opt = [{"id": lb["id"], "name": lb.get("name", ""), "color": lb.get("color", "")} for lb in contenido.get("labels", [])]
                    
                    cards_opt = []
                    for c in contenido.get("cards", []):
                        # Descartamos descripciones largas, acciones, checklists, etc.
                        cards_opt.append({
                            "id": c["id"],
                            "idList": c["idList"],
                            "name": c["name"],
                            "idLabels": c.get("idLabels", []),
                            "pos": c.get("pos", 0),
                            "closed": c.get("closed", False)
                        })

                    # Reconstruimos la data solo con lo esencial
                    data_optimizada = {
                        "lists": listas_opt,
                        "labels": labels_opt,
                        "cards": cards_opt
                    }
                    
                    data_historica.append({
                        "fecha": fecha,
                        "archivo": nombre_archivo,
                        "data": data_optimizada
                    })
            except Exception as e:
                print(f"❌ Error leyendo {nombre_archivo}: {e}")
                
    # Escribir el gran paquete JSON en la raíz
    with open('history_all.json', 'w', encoding='utf-8') as f:
        # Usamos separators=(',', ':') para eliminar los espacios en blanco y reducir aún más el tamaño
        json.dump(data_historica, f, separators=(',', ':'))
        
    print(f"✅ history_all.json generado con éxito con {len(data_historica)} registros.")

if __name__ == "__main__":
    consolidar_historial()
