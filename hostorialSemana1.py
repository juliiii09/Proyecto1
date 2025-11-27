# Lista para almacenar los productos
inventario = []

# Menú principal
print("1. Agregar\n2. Ver\n3. Estadísticas\n4. Salir")
opcion = input("Elige: ")

if opcion == "1":
    print("Agregar producto")
elif opcion == "2":
    print("Ver inventario")
elif opcion == "3":
    print("Ver estadísticas")
elif opcion == "4":
    print("Salir")
else:
    print("Opción inválida")