

import csv
import json
import os
from datetime import datetime, timedelta

# archivos y headers

EQUIPOS_CSV = "equipos_simple.csv"
EQUIPOS_JSON = "equipos_simple.json"
PRESTAMOS_CSV = "prestamos_simple.csv"
PRESTAMOS_JSON = "prestamos_simple.json"

EQUIPOS_HEADER = ["equipo_id", "nombre_equipo", "categoria", "estado_actual", "fecha_registro"]
PRESTAMOS_HEADER = ["prestamo_id","equipo_id","nombre_equipo","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado","mes","anio"]

# reglas para tiempo máximo por tipo de usuario (ejemplo)
TIEMPO_MAX = {"ESTUDIANTE":3, "INSTRUCTOR":7, "ADMINISTRATIVO":10}

#halpers

def hoy_str():
    return datetime.now().strftime("%Y-%m-%d")

def asegurar_csv(path, header):
    """Crea el CSV con cabecera si no existe."""
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)

def leer_csv_dicts(path):
    """Lee CSV y devuelve lista de dicts. Si no existe, []"""
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def escribir_csv_dicts(path, fieldnames, dicts):
    """Sobrescribe CSV con cabecera y dicts."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in dicts:
            writer.writerow(d)

def append_csv_dict(path, fieldnames, row):
    """Añade una fila dict al CSV (crea cabecera si hace falta)."""
    exists = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)

def leer_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def escribir_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def pedir_entero(prompt):
    while True:
        v = input(prompt).strip()
        try:
            return int(v)
        except ValueError:
            print("Escribe un número entero válido.")

def pedir_str_no_vacio(prompt):
    while True:
        s = input(prompt).strip()
        if s != "":
            return s
        print("No puede quedar vacío.")

# --------- Funciones para gestión de equipos ----------
def generar_id(dev_list, key="equipo_id"):
    """Genera siguiente id (string) basado en los ids numéricos existentes."""
    ids = []
    for d in dev_list:
        try:
            ids.append(int(d.get(key, 0)))
        except Exception:
            pass
    return str(max(ids)+1) if ids else "1"

def crear_equipo_csv():
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    nuevo_id = generate = generar_id(equipos, "equipo_id")
    nombre = pedir_str_no_vacio("Nombre del equipo: ")
    categoria = input("Categoría (opcional): ").strip() or "Sin categoría"
    fila = {"equipo_id": nuevo_id, "nombre_equipo": nombre, "categoria": categoria, "estado_actual": "DISPONIBLE", "fecha_registro": hoy_str()}
    append_csv_dict(EQUIPOS_CSV, EQUIPOS_HEADER, fila)
    print("Equipo creado:", fila)

def listar_equipos_csv():
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    if not equipos:
        print("No hay equipos.")
        return
    for e in equipos:
        print(e)

def buscar_equipo_csv():
    q = input("Buscar por ID o parte del nombre: ").strip()
    encontrados = []
    for e in leer_csv_dicts(EQUIPOS_CSV):
        if e["equipo_id"] == q or q.lower() in e["nombre_equipo"].lower():
            encontrados.append(e)
    if not encontrados:
        print("No se encontró.")
    else:
        for r in encontrados:
            print(r)

def editar_equipo_csv():
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    eid = input("ID del equipo a editar: ").strip()
    encontrado = None
    for e in equipos:
        if e["equipo_id"] == eid:
            encontrado = e
            break
    if not encontrado:
        print("Equipo no encontrado.")
        return
    print("Actual:", encontrado)
    nuevo_nombre = input("Nuevo nombre (enter para mantener): ").strip()
    if nuevo_nombre:
        encontrado["nombre_equipo"] = nuevo_nombre
    nueva_cat = input("Nueva categoría (enter para mantener): ").strip()
    if nueva_cat:
        encontrado["categoria"] = nueva_cat
    nuevo_estado = input("Nuevo estado (DISPONIBLE/RESERVADO/PRESTADO) (enter para mantener): ").strip().upper()
    if nuevo_estado:
        encontrado["estado_actual"] = nuevo_estado
    # guardar
    escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
    print("Equipo actualizado.")

def eliminar_equipo_csv():
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    eid = input("ID a eliminar: ").strip()
    nuevos = [e for e in equipos if e["equipo_id"] != eid]
    if len(nuevos) == len(equipos):
        print("ID no encontrado.")
        return
    escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, nuevos)
    print("Eliminado.")

# --------- Funciones para préstamos (CSV simple) ----------
def generar_id_prest(prest_list):
    ids = []
    for p in prest_list:
        try:
            ids.append(int(p.get("prestamo_id", 0)))
        except:
            pass
    return str(max(ids)+1) if ids else "1"

def solicitar_prestamo_csv():
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    eid = input("ID del equipo a solicitar: ").strip()
    equipo = next((x for x in equipos if x["equipo_id"] == eid), None)
    if not equipo:
        print("Equipo no existe.")
        return
    if equipo.get("estado_actual","").upper() != "DISPONIBLE":
        print("Equipo no disponible.")
        return
    usuario = pedir_str_no_vacio("Nombre solicitante: ")
    tipo = input("Tipo (Estudiante/Instructor/Administrativo) [ESTUDIANTE]: ").strip().upper() or "ESTUDIANTE"
    prestamos = leer_csv_dicts(PRESTAMOS_CSV)
    pid = generar_id_prest(prestamos)
    fila = {"prestamo_id": pid, "equipo_id": eid, "nombre_equipo": equipo["nombre_equipo"], "usuario_prestatario": usuario, "tipo_usuario": tipo, "fecha_solicitud": hoy_str(), "fecha_inicio": "", "fecha_fin": "", "dias": "", "retraso": "", "estado": "PENDIENTE", "mes": datetime.now().strftime("%m"), "anio": datetime.now().strftime("%Y")}
    append_csv_dict(PRESTAMOS_CSV, PRESTAMOS_HEADER, fila)
    # marcar reservado
    equipo["estado_actual"] = "RESERVADO"
    escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
    print("Solicitud creada:", fila)

def listar_prestamos_csv():
    prests = leer_csv_dicts(PRESTAMOS_CSV)
    if not prests:
        print("No hay préstamos.")
        return
    for p in prests:
        print(p)

def aprobar_prestamo_csv():
    prestamos = leer_csv_dicts(PRESTAMOS_CSV)
    pid = input("ID préstamo a aprobar: ").strip()
    cambiado = False
    for p in prestamos:
        if p["prestamo_id"] == pid and p["estado"].upper() == "PENDIENTE":
            inicio = hoy_str()
            dias = TIEMPO_MAX.get(p.get("tipo_usuario","").upper(), 3)
            fin = (datetime.strptime(inicio, "%Y-%m-%d") + timedelta(days=dias)).strftime("%Y-%m-%d")
            p["fecha_inicio"] = inicio
            p["fecha_fin"] = fin
            p["dias"] = str(dias)
            p["estado"] = "APROBADO"
            p["mes"] = datetime.now().strftime("%m")
            p["anio"] = datetime.now().strftime("%Y")
            cambiado = True
            # actualizar equipo
            equipos = leer_csv_dicts(EQUIPOS_CSV)
            for e in equipos:
                if e["equipo_id"] == p["equipo_id"]:
                    e["estado_actual"] = "PRESTADO"
            escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
            break
    if cambiado:
        escribir_csv_dicts(PRESTAMOS_CSV, PRESTAMOS_HEADER, prestamos)
        print("Préstamo aprobado.")
    else:
        print("No se aprobó (ID/estado incorrecto).")

def devolver_prestamo_csv():
    prestamos = leer_csv_dicts(PRESTAMOS_CSV)
    pid = input("ID préstamo a devolver: ").strip()
    cambiado = False
    for p in prestamos:
        if p["prestamo_id"] == pid and p["estado"].upper() == "APROBADO":
            if not p.get("fecha_inicio"):
                print("Registro inválido.")
                return
            inicio = datetime.strptime(p["fecha_inicio"], "%Y-%m-%d")
            dias_usados = (datetime.now() - inicio).days
            max_dias = TIEMPO_MAX.get(p.get("tipo_usuario","").upper(), 3)
            retraso = max(0, dias_usados - max_dias)
            p["dias"] = str(dias_usados)
            p["retraso"] = str(retraso)
            p["estado"] = "DEVUELTO"
            p["fecha_fin"] = hoy_str()
            p["mes"] = datetime.now().strftime("%m")
            p["anio"] = datetime.now().strftime("%Y")
            cambiado = True
            # actualizar equipo a disponible
            equipos = leer_csv_dicts(EQUIPOS_CSV)
            for e in equipos:
                if e["equipo_id"] == p["equipo_id"]:
                    e["estado_actual"] = "DISPONIBLE"
            escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
            break
    if cambiado:
        escribir_csv_dicts(PRESTAMOS_CSV, PRESTAMOS_HEADER, prestamos)
        print("Devolución registrada.")
    else:
        print("No se pudo devolver (ID/estado incorrecto).")

# importar y exportar csv

def exportar_equipos_csv_a_json():
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    escribir_json(EQUIPOS_JSON, equipos)
    print(f"Exportado {len(equipos)} equipos a {EQUIPOS_JSON}.")

def importar_equipos_json_a_csv():
    equipos = leer_json(EQUIPOS_JSON)
    if not equipos:
        print("No hay datos en JSON o archivo no existe.")
        return
    escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
    print(f"Importado {len(equipos)} equipos desde {EQUIPOS_JSON}.")

# menu principal

def menu_equipos():
    asegurar_csv(EQUIPOS_CSV, EQUIPOS_HEADER)
    while True:
        print("\n--- MENU EQUIPOS ---")
        print("1) Crear equipo")
        print("2) Listar equipos")
        print("3) Buscar equipo")
        print("4) Editar equipo")
        print("5) Eliminar equipo")
        print("6) Exportar a JSON")
        print("7) Importar desde JSON")
        print("0) Volver")
        op = input("Opción equipos: ").strip()
        if op == "1":
            crear_equipo_csv()
        elif op == "2":
            listar_equipos_csv()
        elif op == "3":
            buscar_equipo_csv()
        elif op == "4":
            editar_equipo_csv()
        elif op == "5":
            eliminar_equipo_csv()
        elif op == "6":
            exportar_equipos_csv_a_json()
        elif op == "7":
            importar_equipos_json_a_csv()
        elif op == "0":
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

def menu_principal():
    # asegurar archivos al inicio (crea si no existen)
    asegurar_csv(EQUIPOS_CSV, EQUIPOS_HEADER)
    asegurar_csv(PRESTAMOS_CSV, PRESTAMOS_HEADER)

    while True:
        print("\n=== MENU PRINCIPAL SIMPLE ===")
        print("1) Gestionar Equipos")
        print("2) Solicitar préstamo")
        print("3) Listar préstamos")
        print("4) Aprobar préstamo")
        print("5) Registrar devolución")
        print("6) Exportar equipos CSV->JSON")
        print("7) Importar equipos JSON->CSV")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_equipos()
        elif op == "2":
            solicitar_prestamo_csv()
        elif op == "3":
            listar_prestamos_csv()
        elif op == "4":
            aprobar_prestamo_csv()
        elif op == "5":
            devolver_prestamo_csv()
        elif op == "6":
            exportar_equipos_csv_a_json()
        elif op == "7":
            importar_equipos_json_a_csv()
        elif op == "0":
            print("Saliendo. ¡Buena suerte en el examen!")
            break
        else:
            print("Opción inválida. Intenta otra vez.")

# --------- Entrada principal ----------
if __name__ == "__main__":
    # crea los archivos si no existen para evitar errores
    asegurar_csv(EQUIPOS_CSV, EQUIPOS_HEADER)
    asegurar_csv(PRESTAMOS_CSV, PRESTAMOS_HEADER)
    menu_principal()

