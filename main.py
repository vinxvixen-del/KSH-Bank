import json

class KSH_Bank:
    def __init__(self):
        self.moneda = "K$H"
        self.usuarios = {}
        self.cargar_datos()

    def cargar_datos(self):
        """Carga datos desde la base de datos JSON"""
        try:
            with open('db_ksh.json', 'r') as f:
                self.usuarios = json.load(f)
        except FileNotFoundError:
            self.usuarios = {"admin": 1000000}
            self.guardar_datos()

    def guardar_datos(self):
        """Guarda datos en la base de datos JSON"""
        with open('db_ksh.json', 'w') as f:
            json.dump(self.usuarios, f, indent=4)

    def validar_monto(self, monto):
        """Valida que el monto sea correcto"""
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                return False, "❌ El monto debe ser mayor a cero."
            return True, monto_float
        except (ValueError, TypeError):
            return False, "❌ El monto debe ser un número válido."

    def transferencia(self, origen, destino, monto):
        """Realiza una transferencia entre cuentas con validación"""
        # Sanitizar nombres de usuario
        origen = str(origen).strip()
        destino = str(destino).strip()

        # Validar monto
        valido, resultado = self.validar_monto(monto)
        if not valido:
            print(resultado)
            return False

        monto = resultado

        # Validaciones
        if origen == destino:
            print("❌ No puedes transferir a la misma cuenta.")
            return False

        if not origen or not destino:
            print("❌ Usuario inválido.")
            return False

        if self.usuarios.get(origen, 0) < monto:
            print("❌ Saldo insuficiente en K$H.")
            return False

        # Realizar transacción
        self.usuarios[origen] -= monto
        self.usuarios[destino] = self.usuarios.get(destino, 0) + monto
        self.guardar_datos()
        print(f"✅ Transacción Exitosa: {monto} {self.moneda} enviados a '{destino}'")
        return True

    def obtener_saldo(self, usuario):
        """Obtiene el saldo de un usuario"""
        return self.usuarios.get(usuario, 0)

    def listar_usuarios(self):
        """Lista todos los usuarios y sus saldos"""
        return self.usuarios


# --- Menú de Operación Interactivo ---
if __name__ == "__main__":
    bank = KSH_Bank()
    print("=" * 40)
    print("🏦 === SISTEMA K$H ACTIVO ===")
    print("=" * 40)
    
    user = input("\n👤 Introduce tu usuario para iniciar sesión: ").strip()

    if not user:
        print("❌ Usuario inválido.")
        exit()

    # Crear usuario si no existe
    if user not in bank.usuarios:
        bank.usuarios[user] = 0
        bank.guardar_datos()
        print(f"✅ Cuenta '{user}' creada con saldo inicial: 0 K$H")

    while True:
        print(f"\n[ Usuario: {user} | Saldo: {bank.obtener_saldo(user)} {bank.moneda} ]")
        print("━" * 40)
        print("1. 💸 Realizar Transferencia")
        print("2. 👥 Ver todos los usuarios (Modo Admin)")
        print("3. 📊 Consultar mi saldo")
        print("4. 🚪 Salir")
        print("━" * 40)
        
        opcion = input("Selecciona una opción (1-4): ").strip()

        if opcion == "1":
            destino = input("👤 Usuario destino: ").strip()
            try:
                monto = float(input("💰 Monto a transferir: "))
                bank.transferencia(user, destino, monto)
            except ValueError:
                print("❌ Por favor, ingresa un número válido para el monto.")
                
        elif opcion == "2":
            print("\n" + "=" * 40)
            print("📋 --- Cuentas Registradas ---")
            print("=" * 40)
            for u, saldo in bank.listar_usuarios().items():
                print(f"  • {u}: {saldo} {bank.moneda}")
            print("=" * 40)
            
        elif opcion == "3":
            print(f"\n💰 Tu saldo actual: {bank.obtener_saldo(user)} {bank.moneda}")

        elif opcion == "4":
            print("\n🙏 ¡Gracias por usar KSH Bank! Cerrando sesión...")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
