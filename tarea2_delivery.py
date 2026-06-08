# =============================================================
# Universidad Andrés Bello - Introducción a la Programación
# Tarea 02 - Sistema de Delivery de Comida Rápida
# Junio 2026
# =============================================================
# Integrantes:
# - Nombre Completo 1  | RUT: XXXXXXXX-X
# - Nombre Completo 2  | RUT: XXXXXXXX-X
# - Nombre Completo 3  | RUT: XXXXXXXX-X
# - Nombre Completo 4  | RUT: XXXXXXXX-X
# - Nombre Completo 5  | RUT: XXXXXXXX-X
# =============================================================

import os
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Constantes: nombres de archivos donde se persisten los datos
# ---------------------------------------------------------------
ARCHIVO_CLIENTES = "clientes.txt"
ARCHIVO_PEDIDOS  = "pedidos.txt"


# ===============================================================
# MÓDULO DE ARCHIVOS                                                                                                                                                                                
# ===============================================================

def guardar_cliente(cliente: dict) -> None:
    """Añade un cliente al archivo de clientes (modo 'a')."""
    with open(ARCHIVO_CLIENTES, "a", encoding="utf-8") as f:
        f.write(
            f"{cliente['rut']}|"
            f"{cliente['primer_nombre']}|"
            f"{cliente['segundo_nombre']}|"
            f"{cliente['apellido_paterno']}|"
            f"{cliente['apellido_materno']}|"
            f"{cliente['telefono']}|"
            f"{cliente['email']}|"
            f"{cliente['direccion']}|"
            f"{cliente['monto_disponible']}\n"
        )


def leer_clientes() -> list:
    """Lee todos los clientes desde el archivo y retorna lista de dicts."""
    clientes = []
    if not os.path.exists(ARCHIVO_CLIENTES):
        return clientes
    with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            campos = linea.split("|")
            if len(campos) == 9:
                clientes.append({
                    "rut":              campos[0],
                    "primer_nombre":    campos[1],
                    "segundo_nombre":   campos[2],
                    "apellido_paterno": campos[3],
                    "apellido_materno": campos[4],
                    "telefono":         campos[5],
                    "email":            campos[6],
                    "direccion":        campos[7],
                    "monto_disponible": float(campos[8]),
                })
    return clientes


def guardar_pedido(pedido: dict) -> None:
    """Añade un pedido al archivo de pedidos (modo 'a')."""
    with open(ARCHIVO_PEDIDOS, "a", encoding="utf-8") as f:
        f.write(
            f"{pedido['rut']}|"
            f"{pedido['codigo']}|"
            f"{pedido['nombre_producto']}|"
            f"{pedido['categoria']}|"
            f"{pedido['cantidad']}|"
            f"{pedido['precio_unitario']}|"
            f"{pedido['costo_total']}\n"
        )


def leer_pedidos() -> list:
    """Lee todos los pedidos desde el archivo y retorna lista de dicts."""
    pedidos = []
    if not os.path.exists(ARCHIVO_PEDIDOS):
        return pedidos
    with open(ARCHIVO_PEDIDOS, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            campos = linea.split("|")
            if len(campos) == 7:
                pedidos.append({
                    "rut":             campos[0],
                    "codigo":          campos[1],
                    "nombre_producto": campos[2],
                    "categoria":       campos[3],
                    "cantidad":        int(campos[4]),
                    "precio_unitario": float(campos[5]),
                    "costo_total":     float(campos[6]),
                })
    return pedidos


def actualizar_monto_cliente(rut: str, nuevo_monto: float) -> None:
    """Reescribe el archivo de clientes actualizando el monto del cliente indicado."""
    clientes = leer_clientes()
    with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as f:
        for c in clientes:
            if c["rut"] == rut:
                c["monto_disponible"] = nuevo_monto
            f.write(
                f"{c['rut']}|"
                f"{c['primer_nombre']}|"
                f"{c['segundo_nombre']}|"
                f"{c['apellido_paterno']}|"
                f"{c['apellido_materno']}|"
                f"{c['telefono']}|"
                f"{c['email']}|"
                f"{c['direccion']}|"
                f"{c['monto_disponible']}\n"
            )


# ===============================================================
# MÓDULO DE BÚSQUEDA / UTILIDADES
# ===============================================================

def buscar_cliente_por_rut(rut: str, clientes: list) -> dict | None:
    """Retorna el dict del cliente cuyo rut coincide, o None si no existe."""
    for cliente in clientes:
        if cliente["rut"] == rut:
            return cliente
    return None


def calcular_costo_total(cantidad: int, precio_unitario: float) -> float:
    """Calcula y retorna el costo total de un pedido."""
    return cantidad * precio_unitario


# ===============================================================
# MÓDULO DE ENTRADA DE DATOS
# ===============================================================

def ingresar_cliente() -> None:
    """Solicita los datos de un cliente y los persiste en el archivo."""
    print("\nIngrese los siguientes datos")

    rut             = input("Rut: ").strip()
    primer_nombre   = input("Primer nombre: ").strip()
    segundo_nombre  = input("Segundo nombre: ").strip()
    apell_paterno   = input("Apellido paterno: ").strip()
    apell_materno   = input("Apellido materno: ").strip()
    telefono        = input("Teléfono: ").strip()
    email           = input("Email: ").strip()
    direccion       = input("Dirección de entrega: ").strip()

    while True:
        try:
            monto = float(input("Monto disponible para compra : ").strip())
            break
        except ValueError:
            print("Error: ingrese un número válido para el monto.")

    cliente = {
        "rut":              rut,
        "primer_nombre":    primer_nombre,
        "segundo_nombre":   segundo_nombre,
        "apellido_paterno": apell_paterno,
        "apellido_materno": apell_materno,
        "telefono":         telefono,
        "email":            email,
        "direccion":        direccion,
        "monto_disponible": monto,
    }

    guardar_cliente(cliente)
    print("Cliente registrado correctamente.")


def ingresar_pedido() -> None:
    """
    Solicita el RUT del cliente y los datos del pedido.
    Repite la solicitud de cantidad y precio mientras el costo supere
    el monto disponible del cliente.
    """
    print("\nIngrese los siguientes datos:")

    rut = input("Rut: ").strip()

    clientes = leer_clientes()
    cliente  = buscar_cliente_por_rut(rut, clientes)

    if cliente is None:
        print("Error: no existe un cliente con ese RUT.")
        return

    codigo          = input("Código del pedido: ").strip()
    nombre_producto = input("Nombre del producto: ").strip()
    categoria       = input("Categoría: ").strip()

    monto_disponible = cliente["monto_disponible"]

    while True:
        try:
            cantidad = int(input("Cantidad: ").strip())
            precio   = float(input("Precio unitario: ").strip())
        except ValueError:
            print("Error: ingrese valores numéricos válidos.")
            continue

        costo_total = calcular_costo_total(cantidad, precio)

        if costo_total > monto_disponible:
            print(
                f"Su monto disponible para compra es de {int(monto_disponible)}, "
                f"el costo total del pedido es de {int(costo_total)}"
            )
        else:
            break

    print(f"Costo total: {int(costo_total)} (dato calculado)")

    pedido = {
        "rut":             rut,
        "codigo":          codigo,
        "nombre_producto": nombre_producto,
        "categoria":       categoria,
        "cantidad":        cantidad,
        "precio_unitario": precio,
        "costo_total":     costo_total,
    }

    guardar_pedido(pedido)

    # Descontar monto al cliente
    nuevo_monto = monto_disponible - costo_total
    actualizar_monto_cliente(rut, nuevo_monto)

    print("Pedido registrado correctamente.")


# ===============================================================
# MÓDULO DE VISUALIZACIÓN
# ===============================================================

def visualizar_clientes() -> None:
    """Muestra en pantalla los datos de todos los clientes registrados."""
    clientes = leer_clientes()
    if not clientes:
        print("\nNo hay clientes registrados.")
        return

    print("\nVisualización de los datos de los clientes")
    for c in clientes:
        print(f"Rut: {c['rut']}")
        print(f"Primer nombre: {c['primer_nombre']}")
        print(f"Segundo nombre: {c['segundo_nombre']}")
        print(f"Apellido paterno: {c['apellido_paterno']}")
        print(f"Apellido materno: {c['apellido_materno']}")
        print(f"Teléfono: {c['telefono']}")
        print(f"Email: {c['email']}")
        print(f"Dirección de entrega: {c['direccion']}")
        print(f"Monto disponible para compra : {int(c['monto_disponible'])}")
        print()


def visualizar_pedidos() -> None:
    """Muestra en pantalla los datos de todos los pedidos registrados."""
    pedidos = leer_pedidos()
    if not pedidos:
        print("\nNo hay pedidos registrados.")
        return

    print("\nVisualización de los datos de los pedidos")
    for p in pedidos:
        print(f"Rut: {p['rut']}")
        print(f"Código del pedido: {p['codigo']}")
        print(f"Nombre del producto: {p['nombre_producto']}")
        print(f"Categoría: {p['categoria']}")
        print(f"Cantidad: {p['cantidad']}")
        print(f"Precio unitario: {int(p['precio_unitario'])}")
        print(f"Costo total: {int(p['costo_total'])} (dato calculado)")
        print()


def visualizar_grafico() -> None:
    """Genera y muestra un gráfico de barras con el monto disponible por cliente."""
    clientes = leer_clientes()
    if not clientes:
        print("\nNo hay clientes registrados para graficar.")
        return

    print("\nGráfico del monto disponible para compra de los clientes")

    nombres = [
        f"{c['primer_nombre']} {c['apellido_paterno']}"
        for c in clientes
    ]
    montos = [c["monto_disponible"] for c in clientes]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(nombres, montos, color="steelblue")
    ax.set_title("Gráfico de Barras")
    ax.set_xlabel("Clientes")
    ax.set_ylabel("Monto disponible")
    plt.tight_layout()
    plt.show()


# ===============================================================
# MENÚ PRINCIPAL
# ===============================================================

def mostrar_menu() -> None:
    """Imprime el menú de opciones."""
    print("\nSISTEMA DE DELIVERY DE COMIDA RÁPIDA")
    print("1. Ingresar datos de clientes")
    print("2. Ingresar pedidos de comida rápida")
    print("3. Visualizar datos de clientes")
    print("4. Visualizar pedidos registrados")
    print("5. Visualizar gráfico del monto disponible de los clientes")
    print("6. Salir del programa")


def ejecutar_opcion(opcion: str) -> bool:
    """
    Ejecuta la acción correspondiente a la opción elegida.
    Retorna False cuando el usuario elige salir, True en caso contrario.
    """
    if opcion == "1":
        ingresar_cliente()
    elif opcion == "2":
        ingresar_pedido()
    elif opcion == "3":
        visualizar_clientes()
    elif opcion == "4":
        visualizar_pedidos()
    elif opcion == "5":
        visualizar_grafico()
    elif opcion == "6":
        print("Fin de la ejecución del programa")
        return False
    else:
        print("Opción no válida. Intente nuevamente.")
    return True


def main() -> None:
    """Punto de entrada principal del programa."""
    continuar = True
    while continuar:
        mostrar_menu()
        opcion = input("Seleccione su opción: ").strip()
        continuar = ejecutar_opcion(opcion)


# ===============================================================
if __name__ == "__main__":
    main()
