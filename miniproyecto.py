import json
import os
#import csv

ARCHIVO = "estudiantes.json" # archivo json


def leerEstudiantes():
 
    if not os.path.exists(ARCHIVO):
        return []
    
 #buscar errores
    try:
        with open(ARCHIVO, "r") as jason:
            return json.load(jason) # convierte el archivo json a uno legible para python (diccionario, lista)
    except json.JSONDecodeError:
        return []
    
   
def guardarEstudiantes(lista):
   
    with open(ARCHIVO, "w") as jason:
        json.dump(lista, jason, indent=4) #indentacion de 4 espacios para que sea mas legible. escribe la lista en formato json

        

def crearEstudiante():

    estudiantes = leerEstudiantes() #lista actual

    nombre = input("Nombre del estudiante: ")

    nuevo_id = 1 if not estudiantes else estudiantes[-1]["id"] + 1

   #diccionario del nuevo estudiante
    nuevo = {
        "id": nuevo_id,
        "nombre": nombre
    }
  
    # Agregarlo a la lista en json
    estudiantes.append(nuevo)

    # Guardar cambios en el archivo
    guardarEstudiantes(estudiantes)
    print("Estudiante agregado con exito")


def actualizarEstudiante():
   
    estudiantes = leerEstudiantes()

    idBuscar = int(input("ID del estudiante a actualizar: "))

    # Buscar alumno dentro de la lista
    for estudiante in estudiantes:
      if estudiante["id"] == idBuscar:
        nuevoNombre = input("Nuevo nombre: ")

          
        estudiante["nombre"] = nuevoNombre

            
        guardarEstudiantes(estudiantes)
        print("Estudiante actualizado")
        return 
    # Si no se encontró
    print("No existe un estudiante con ese ID")



def eliminarEstudiante():
    estudiantes = leerEstudiantes()
    idDelete = int(input("ID del estudiante a eliminar: "))

    # lista sin el idDelete
    nuevos = [e for e in estudiantes if e["id"] != idDelete]

    #si las listas quedan con el mismo tamaño, entonces no se borro ningún estudiante
    if len(nuevos) == len(estudiantes):
        print("No existe un estudiante con ese ID")
        return

    guardarEstudiantes(nuevos)
    print("Estudiante eliminado")

def menu():
    while True:
        print("\nMENU PRINCIPAL")
        print("1. Ver estudiantes")
        print("2. Crear estudiante")
        print("3. Actualizar estudiante")
        print("4. Eliminar estudiante")
        print("5. Salir")

        opc = input("Elige una opción: ")

        if opc == "1":
            print(leerEstudiantes())          
        elif opc == "2":
            crearEstudiante()                
        elif opc == "3":
            actualizarEstudiante()               
        elif opc == "4":
            eliminarEstudiante()                
        elif opc == "5":
            print("Saliendo.")
            break                              
        else:
            print("Opción incorrecta")          

menu()
