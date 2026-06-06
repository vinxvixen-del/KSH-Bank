import json

class KSH_Bank:
    def __init__(self):
        self.moneda = "K$H"
        self.usuarios = {}  # Aquí se guardarán los saldos
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open('db_ksh.json', 'r') as f:
                self.usuarios = json.load(f)
        except FileNotFoundError:
            # Si el archivo no existe, creamos el admin con fondos
            self.usuarios = {"admin": 1000000}
            self.guardar_datos()

    def guardar_datos(self):
        with open('db_ksh.json', 'w') as f:
            json.dump(self.usuarios, f, indent=4)

    def transferencia(self, origen, destino, monto):
        if monto <= 0:
            print("❌ El monto debe ser mayor a cero.")
            return

        if self.usuarios.get(origen, 0) >= monto:
            self.usuarios[origen] -= monto
            self.usuarios[destino] = self.usuarios.get(destino, 0) + monto
            self.guardar_datos()
            print(f"\n✅ Transacción Exitosa: {monto} {self.moneda} enviados a '{destino}'")
        else:
            print("\n❌ Saldo insuficiente en K$H.")

# --- Menú de Operación Interactivo ---
bank = KSH_Bank()
print("=== SISTEMA K$H ACTIVO ===")
user = input("Introduce tu usuario para iniciar sesión: ").strip()

# Si el usuario no existe en la base de datos, inicia con 0 K$H
if user not in bank.usuarios:
    bank.usuarios[user] = 0
    bank.guardar_datos()

while True:
    print(f"\n[ Usuario: {user} | Saldo: {bank.usuarios.get(user, 0)} {bank.moneda} ]")
    print("1. Realizar Transferencia")
    print("2. Ver todos los usuarios (Modo Admin)")
    print("3. Salir")
    
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        destino = input("Usuario destino: ").strip()
        try:
            monto = float(input("Monto a transferir: "))
            bank.transferencia(user, destino, monto)
        except ValueError:
            print("❌ Por favor, ingresa un número válido para el monto.")
            
    elif opcion == "2":
        print("\n--- Cuentas registradas ---")
        for u, saldo in bank.usuarios.items():
            print(f"- {u}: {saldo} {bank.moneda}")
            
    elif opcion == "3":
        print("¡Gracias por usar KSH Bank! Cerrando sesión...")
        break
    else:
        print("❌ Opción inválida.")
