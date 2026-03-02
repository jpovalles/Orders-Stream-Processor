import requests
import json

BASE_URL = "http://api:8001"  # Cambiar esto si la API está en otro host/puerto


def print_response(resp):
    print(f"\n  Status: {resp.status_code}")
    try:
        data = resp.json()
        print("  Respuesta:")
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception:
        print(f"  Respuesta: {resp.text}")


# ──────────────── TASKS ────────────────

def list_tasks():
    print("\n[GET /tasks]")
    resp = requests.get(f"{BASE_URL}/tasks")
    print_response(resp)


def get_task():
    print("\n[GET /tasks/{task_id}]")
    task_id = input("  task_id: ").strip()
    if not task_id.isdigit():
        print("  X Ingresa un número válido.")
        return
    resp = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print_response(resp)


# ──────────────── ORDERS ────────────────

def list_orders():
    print("\n[GET /orders]")
    resp = requests.get(f"{BASE_URL}/orders")
    print_response(resp)


def create_order():
    print("\n[POST /orders]")
    product = input("  Producto: ").strip()
    qty = input("  Cantidad: ").strip()
    if not qty.isdigit():
        print("  X La cantidad debe ser un número entero.")
        return
    payload = {"product": product, "product_quantity": int(qty)}
    resp = requests.post(f"{BASE_URL}/orders", json=payload)
    print_response(resp)


def delete_order():
    print("\n[DELETE /orders/{order_id}]")
    order_id = input("  order_id: ").strip()
    if not order_id.isdigit():
        print("  X Ingresa un número válido.")
        return
    confirm = input(f"  ¿Eliminar orden {order_id}? (s/n): ").strip().lower()
    if confirm != "s":
        print("  Operación cancelada.")
        return
    resp = requests.delete(f"{BASE_URL}/orders/{order_id}")
    print_response(resp)


# ──────────────── MENÚ ────────────────

MENU = """
╔══════════════════════════════════════╗
║         CLIENTE API - MENÚ           ║
╠══════════════════════════════════════╣
║  TASKS                               ║
║  1. Listar todas las tasks           ║
║  2. Obtener task por ID              ║
╠══════════════════════════════════════╣
║  ORDERS                              ║
║  3. Listar todas las órdenes         ║
║  4. Crear orden                      ║
║  5. Eliminar orden                   ║
╠══════════════════════════════════════╣
║  0. Salir                            ║
╚══════════════════════════════════════╝
"""

ACTIONS = {
    "1": list_tasks,
    "2": get_task,
    "3": list_orders,
    "4": create_order,
    "5": delete_order,
}


def main():
    print(f"\n  API Client iniciado → {BASE_URL}")
    while True:
        print(MENU)
        choice = input("  Selecciona una opción: ").strip()
        if choice == "0":
            print("\n  Hasta luego.\n")
            break
        action = ACTIONS.get(choice)
        if action:
            try:
                action()
            except requests.exceptions.ConnectionError:
                print(f"\n  X No se pudo conectar a {BASE_URL}. Verifica que la API esté corriendo.")
            except Exception as e:
                print(f"\n  X Error inesperado: {e}")
        else:
            print("\n  X Opción no válida, intenta de nuevo.")
        input("\n  [Enter para continuar]")


if __name__ == "__main__":
    main()