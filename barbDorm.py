import threading
import time
import random

class BarberoDormilon:
    def __init__(self, total_sillas):
        self.sillas_disponibles = total_sillas
        self.total_sillas = total_sillas
        self.cliente_esperando = threading.Semaphore(0)
        self.barbero_disponible = threading.Semaphore(0)
        self.mutex = threading.Lock()
        self.ejecutando = True

    def barbero(self):
        print("Barbero: Comenzando el día de trabajo")
        
        while self.ejecutando:
            print("Barbero: Esperando clientes (dormido)...")
            self.cliente_esperando.acquire()
            
            with self.mutex:
                if not self.ejecutando:
                    break
            
            print("Barbero: Cortando el pelo a un cliente")
            time.sleep(random.uniform(2, 5))
            
            print("Barbero: Terminé de cortar el pelo")
            
            self.barbero_disponible.release()
        
        print("Barbero: Cerrando la barbería")

    def cliente(self, id_cliente):
        print(f"Cliente {id_cliente}: Llegando a la barbería")
        
        with self.mutex:
            if self.sillas_disponibles > 0:
                self.sillas_disponibles -= 1
                print(f"Cliente {id_cliente}: Esperando en la sala. Sillas disponibles: {self.sillas_disponibles}")
                self.cliente_esperando.release()
            else:
                print(f"Cliente {id_cliente}: No hay sillas disponibles. Me voy sin corte de pelo")
                return

        print(f"Cliente {id_cliente}: Esperando a que el barbero me atienda")
        self.barbero_disponible.acquire()

        with self.mutex:
            self.sillas_disponibles += 1
            print(f"Cliente {id_cliente}: Me están cortando el pelo. Sillas disponibles: {self.sillas_disponibles}")
        
        print(f"Cliente {id_cliente}: Me voy con mi nuevo corte de pelo")

    def iniciar_simulacion(self, num_clientes, intervalo_min=1, intervalo_max=5):
        hilo_barbero = threading.Thread(target=self.barbero)
        hilo_barbero.start()
        
        hilos_clientes = []
        for i in range(num_clientes):
            time.sleep(random.uniform(intervalo_min, intervalo_max))
            hilo_cliente = threading.Thread(target=self.cliente, args=(i,))
            hilo_cliente.start()
            hilos_clientes.append(hilo_cliente)
        
        for hilo in hilos_clientes:
            hilo.join()
        
        with self.mutex:
            self.ejecutando = False
            self.cliente_esperando.release()  # Desbloquea al barbero para que termine
        
        hilo_barbero.join()
        
        print("Simulación finalizada")

if __name__ == "__main__":
    barberia = BarberoDormilon(3)
    
    print("Iniciando simulación del Barbero Dormilón")
    barberia.iniciar_simulacion(10)
