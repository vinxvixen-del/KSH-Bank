import json
import time

class KSH_Bank:
    def __init__(self):
        self.moneda = "K$H"
        self.usuarios = {} # Aquí se guardarán los saldos
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open('db_ksh.json', 'r') as f:
                self.usuarios = json.load(f)
        except FileNotFoundError:            self.usuarios = {"admin": 1000000} # Reserva inicial

    def guardar_datos(self):
        with open('db_ksh.json', 'w') as f:
            json.dump(self.usuarios, f, indent=4)

    def transferencia(self, origen, destino, monto):
        if self.usuarios.get(origen, 0) >= monto:
            self.usuarios[origen] -= monto
            self.usuarios[destino] = self.usuarios.get(destino, 0) + monto
            self.guardar_datos()
            print(f"✅ Transacción Exitosa: {monto} {self.moneda} enviados a {destino}")
        else:
            print("❌ Saldo insuficiente en K$H.")

# --- Menú de Operación ---
bank = KSH_Bank()
print("--- SISTEMA K$H ACTIVO ---")
user = input("Usuario: ")
print(f"Saldo actual: {bank.usuarios.get(user, 0)} K$H")

