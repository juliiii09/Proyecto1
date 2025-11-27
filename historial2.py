

# Lista para almacenar los productos como diccionarios
inventario = []


#  agregar un producto al inventario
def agregar_producto(inventario):
    """Pide nombre, precio y cantidad; valida los datos y añade el producto a la lista."""
    
    # Pedir y validar nombre
    nombre = input("Nombre del producto: ").strip()
    while not nombre:
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre del producto: ").strip()

    # Pedir precio y validar
    while True:
        precio = input("Precio: ")
        try:
            precio = float(precio)
            if precio < 0:
                print("El precio debe ser positivo.")
                continue
            break
        except ValueError:
            print("Precio inválido. Escribe un número (ej. 12.50).")

    # Pedir cantidad y validar (
    while True:
        cantidad = input("Cantidad: ")
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                print("La cantidad debe ser 0 o mayor.")
                continue
            break
        except ValueError:
            print("Cantidad inválida. Escribe un entero (ej. 3).")

    #  diccionario del producto 
    producto = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
    inventario.append(producto)
    print("Producto agregado correctamente.\n")


# Función para mostrar todos los productos del inventario
def mostrar_inventario(inventario):
   
    if not inventario:
        print("El inventario está vacío.\n")
        return
    
    print("\n -INVENTARIO-")
    for p in inventario:
        print(f"Producto: {p['nombre']} | Precio: {p['precio']} | Cantidad: {p['cantidad']}")
    print()


# Función para calcular estadísticas del inventario
def calcular_estadisticas(inventario):
    """Calcula el valor total y la cantidad total de productos."""
    
    if not inventario:
        print("El inventario está vacío.\n")
        return
    
    suma_total = 0
    cantidad_total = 0

    # Sumar precio × cantidad de cada producto 
    for p in inventario:
        suma_total += p["precio"] * p["cantidad"]
        cantidad_total += p["cantidad"]

    print("\n--- ESTADÍSTICAS ---")
    print(f"Valor total del inventario: ${suma_total}")
    print(f"Cantidad total de productos: {cantidad_total}\n")


# Programa principal
def main():
    """Menú principal con bucle while que continúa hasta que el usuario elige salir."""
    
    print("=== SISTEMA DE INVENTARIO ===\n")
    
    # Bucle principal 
    while True:
        print("1. Agregar producto")
        print("2. Ver inventario")
        print("3. Ver estadísticas")
        print("4. Salir")
        
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            agregar_producto(inventario)
        elif opcion == "2":
            mostrar_inventario(inventario)
        elif opcion == "3":
            calcular_estadisticas(inventario)
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.\n")


# Ejecutar el programa
if __name__ == "__main__":
    main()






















