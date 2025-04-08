"""
Implementación de problemas clásicos de concurrencia usando Python threading
"""
import threading
import time
import random
from collections import deque
from queue import Queue


class Buffer:
    def __init__(self, size):
        self.buffer = Queue(maxsize=size)
        self.mutex = threading.Lock()
        
    def produce(self, item):
        self.buffer.put(item)
        
    def consume(self):
        return self.buffer.get()
        
    def is_full(self):
        return self.buffer.full()
        
    def is_empty(self):
        return self.buffer.empty()

def productor(buffer, num_items):
    for i in range(num_items):
        item = f"Item-{i}"
        buffer.produce(item)
        print(f"Productor: Produjo {item}")
        time.sleep(random.uniform(0.1, 0.5))
    print("Productor: Terminó")

def consumidor(buffer, num_items):
    for i in range(num_items):
        item = buffer.consume()
        print(f"Consumidor: Consumió {item}")
        time.sleep(random.uniform(0.2, 0.7))
    print("Consumidor: Terminó")

def ejecutar_productor_consumidor():
    print("\n--- Ejecutando Problema Productor-Consumidor ---")
    buffer = Buffer(5)
    num_items = 10
    
    productor_thread = threading.Thread(target=productor, args=(buffer, num_items))
    consumidor_thread = threading.Thread(target=consumidor, args=(buffer, num_items))
    
    productor_thread.start()
    consumidor_thread.start()
    
    productor_thread.join()
    consumidor_thread.join()
    print("Problema Productor-Consumidor completado")


class Filosofo(threading.Thread):
    def __init__(self, id, tenedor_izq, tenedor_der, comidas_restantes):
        threading.Thread.__init__(self)
        self.id = id
        self.tenedor_izq = tenedor_izq
        self.tenedor_der = tenedor_der
        self.comidas_restantes = comidas_restantes
        
    def pensar(self):
        print(f"Filósofo {self.id} está pensando...")
        time.sleep(random.uniform(0.1, 0.5))
        
    def comer(self):
        print(f"Filósofo {self.id} está comiendo...")
        time.sleep(random.uniform(0.5, 1))
        self.comidas_restantes -= 1
        print(f"Filósofo {self.id} terminó de comer, le quedan {self.comidas_restantes} comidas")
        
    def run(self):
        while self.comidas_restantes > 0:
            self.pensar()
            
            # Intenta tomar los tenedores (solución para evitar deadlock)
            if self.id % 2 == 0:  # Filósofos pares toman primero izquierda, luego derecha
                print(f"Filósofo {self.id} intenta tomar tenedor izquierdo")
                self.tenedor_izq.acquire()
                print(f"Filósofo {self.id} tomó tenedor izquierdo")
                print(f"Filósofo {self.id} intenta tomar tenedor derecho")
                self.tenedor_der.acquire()
                print(f"Filósofo {self.id} tomó tenedor derecho")
            else:  # Filósofos impares toman primero derecha, luego izquierda
                print(f"Filósofo {self.id} intenta tomar tenedor derecho")
                self.tenedor_der.acquire()
                print(f"Filósofo {self.id} tomó tenedor derecho")
                print(f"Filósofo {self.id} intenta tomar tenedor izquierdo")
                self.tenedor_izq.acquire()
                print(f"Filósofo {self.id} tomó tenedor izquierdo")
                
            # Come
            self.comer()
            
            # Libera los tenedores
            self.tenedor_izq.release()
            print(f"Filósofo {self.id} liberó tenedor izquierdo")
            self.tenedor_der.release()
            print(f"Filósofo {self.id} liberó tenedor derecho")

def ejecutar_filosofos_comensales():
    print("\n--- Ejecutando Problema de los Filósofos Comensales ---")
    num_filosofos = 5
    comidas_por_filosofo = 3
    
    # Crear los tenedores (semáforos)
    tenedores = [threading.Lock() for _ in range(num_filosofos)]
    
    # Crear los filósofos
    filosofos = []
    for i in range(num_filosofos):
        # Cada filósofo toma el tenedor a su izquierda y derecha
        tenedor_izq = tenedores[i]
        tenedor_der = tenedores[(i + 1) % num_filosofos]
        filosofo = Filosofo(i, tenedor_izq, tenedor_der, comidas_por_filosofo)
        filosofos.append(filosofo)
    
    # Comenzar a los filósofos
    for filosofo in filosofos:
        filosofo.start()
    
    # Esperar a que terminen
    for filosofo in filosofos:
        filosofo.join()
    
    print("Problema de los Filósofos Comensales completado")



class GestorBD:
    def __init__(self):
        self.lectores = 0
        self.escritores = 0
        self.mutex_lectores = threading.Lock()
        self.mutex_escritores = threading.Lock()
        self.recurso_bd = threading.Lock()
        
    def iniciar_lectura(self):
        with self.mutex_lectores:
            if self.lectores == 0:
                # Primer lector adquiere el lock de la BD
                self.recurso_bd.acquire()
            self.lectores += 1
            print(f"Lector empieza a leer. Total lectores: {self.lectores}")
    
    def terminar_lectura(self):
        with self.mutex_lectores:
            self.lectores -= 1
            print(f"Lector termina de leer. Total lectores: {self.lectores}")
            if self.lectores == 0:
                # Último lector libera el lock de la BD
                self.recurso_bd.release()
    
    def iniciar_escritura(self):
        self.mutex_escritores.acquire()
        self.escritores += 1
        print(f"Escritor espera para escribir. Total escritores esperando: {self.escritores}")
        self.mutex_escritores.release()
        
        # Adquirir acceso exclusivo a la BD
        self.recurso_bd.acquire()
        print("Escritor comienza a escribir")
    
    def terminar_escritura(self):
        print("Escritor termina de escribir")
        self.mutex_escritores.acquire()
        self.escritores -= 1
        self.mutex_escritores.release()
        self.recurso_bd.release()

def lector(id, gestor, num_lecturas):
    for i in range(num_lecturas):
        # Piensa antes de leer
        time.sleep(random.uniform(0.1, 1))
        
        # Lee
        gestor.iniciar_lectura()
        print(f"Lector {id} está leyendo (lectura {i+1}/{num_lecturas})")
        time.sleep(random.uniform(0.2, 0.5))
        gestor.terminar_lectura()

def escritor(id, gestor, num_escrituras):
    for i in range(num_escrituras):
        # Piensa antes de escribir
        time.sleep(random.uniform(0.3, 1.5))
        
        # Escribe
        gestor.iniciar_escritura()
        print(f"Escritor {id} está escribiendo (escritura {i+1}/{num_escrituras})")
        time.sleep(random.uniform(0.5, 1))
        gestor.terminar_escritura()

def ejecutar_lectores_escritores():
    print("\n--- Ejecutando Problema de Lectores-Escritores ---")
    gestor = GestorBD()
    
    num_lectores = 5
    num_escritores = 2
    lecturas_por_lector = 3
    escrituras_por_escritor = 2
    
    lectores = []
    escritores = []
    
    # Crear lectores
    for i in range(num_lectores):
        t = threading.Thread(target=lector, args=(i, gestor, lecturas_por_lector))
        lectores.append(t)
        
    # Crear escritores
    for i in range(num_escritores):
        t = threading.Thread(target=escritor, args=(i, gestor, escrituras_por_escritor))
        escritores.append(t)
    
    # Iniciar todos los hilos
    for t in lectores + escritores:
        t.start()
        
    # Esperar a que terminen
    for t in lectores + escritores:
        t.join()
    
    print("Problema de Lectores-Escritores completado")


class Barberia:
    def __init__(self, num_sillas):
        self.barbero_durmiendo = True
        self.silla_barbero_ocupada = False
        self.sillas_disponibles = num_sillas
        self.mutex = threading.Lock()
        self.barbero_disponible = threading.Semaphore(0)
        self.cliente_listo = threading.Semaphore(0)
        self.corte_terminado = threading.Semaphore(0)
    
    def barbero_thread(self, num_clientes_max):
        clientes_atendidos = 0
        
        while clientes_atendidos < num_clientes_max:
            print("Barbero: Esperando clientes...")
            
            # Barbero espera cliente
            self.cliente_listo.acquire()
            
            # Corta pelo
            print("Barbero: Cortando pelo al cliente")
            time.sleep(random.uniform(0.5, 2))
            
            # Termina corte
            print("Barbero: Terminó el corte")
            self.corte_terminado.release()
            clientes_atendidos += 1
    
    def cliente_thread(self, id_cliente):
        print(f"Cliente {id_cliente}: Llega a la barbería")
        
        with self.mutex:
            if self.sillas_disponibles > 0:
                self.sillas_disponibles -= 1
                print(f"Cliente {id_cliente}: Se sienta en la sala de espera. Sillas disponibles: {self.sillas_disponibles}")
            else:
                print(f"Cliente {id_cliente}: La barbería está llena, se va")
                return
        
        # Avisa al barbero que hay un cliente
        self.cliente_listo.release()
        
        # Espera a que el barbero termine el corte
        print(f"Cliente {id_cliente}: Pasa a la silla del barbero")
        self.corte_terminado.acquire()
        print(f"Cliente {id_cliente}: Recibió su corte y se va")
        
        with self.mutex:
            self.sillas_disponibles += 1
            print(f"Se liberó una silla. Sillas disponibles: {self.sillas_disponibles}")

def ejecutar_barbero_dormilon():
    print("\n--- Ejecutando Problema del Barbero Dormilón ---")
    num_sillas = 3
    num_clientes = 10
    barberia = Barberia(num_sillas)
    
    # Crear y empezar el hilo del barbero
    barbero = threading.Thread(target=barberia.barbero_thread, args=(num_clientes,))
    barbero.start()
    
    # Crear y empezar hilos de clientes
    clientes = []
    for i in range(num_clientes):
        cliente = threading.Thread(target=barberia.cliente_thread, args=(i,))
        clientes.append(cliente)
        cliente.start()
        # Tiempo aleatorio entre llegadas de clientes
        time.sleep(random.uniform(0.1, 1))
    
    # Esperar a que terminen todos los hilos
    for cliente in clientes:
        cliente.join()
    
    barbero.join()
    print("Problema del Barbero Dormilón completado")


class CintaTransportadora:
    def __init__(self, capacidad):
        self.items = deque()
        self.capacidad = capacidad
        self.mutex = threading.Lock()
        self.no_llena = threading.Condition(self.mutex)
        self.no_vacia = threading.Condition(self.mutex)
    
    def producir(self, productor_id, item):
        with self.mutex:
            while len(self.items) >= self.capacidad:
                print(f"Productor {productor_id}: Cinta llena, esperando...")
                self.no_llena.wait()
            
            self.items.append(item)
            print(f"Productor {productor_id}: Colocó {item} en la cinta. Tamaño: {len(self.items)}/{self.capacidad}")
            
            # Notificar a los consumidores que hay un elemento disponible
            self.no_vacia.notify()
    
    def consumir(self, consumidor_id):
        with self.mutex:
            while len(self.items) == 0:
                print(f"Consumidor {consumidor_id}: Cinta vacía, esperando...")
                self.no_vacia.wait()
            
            item = self.items.popleft()
            print(f"Consumidor {consumidor_id}: Retiró {item} de la cinta. Tamaño: {len(self.items)}/{self.capacidad}")
            
            # Notificar a los productores que hay espacio disponible
            self.no_llena.notify()
            
            return item

def productor_multiple(cinta, id, num_items):
    for i in range(num_items):
        item = f"P{id}-Item{i}"
        # Tiempo aleatorio para producir
        time.sleep(random.uniform(0.1, 0.5))
        cinta.producir(id, item)
    
    print(f"Productor {id}: Ha terminado de producir")

def consumidor_multiple(cinta, id, num_items):
    for i in range(num_items):
        # Tiempo aleatorio para consumir
        time.sleep(random.uniform(0.3, 0.8))
        item = cinta.consumir(id)
    
    print(f"Consumidor {id}: Ha terminado de consumir")

def ejecutar_cinta_transportadora():
    print("\n--- Ejecutando Problema de la Cinta Transportadora ---")
    capacidad_cinta = 5
    num_productores = 3
    num_consumidores = 2
    items_por_productor = 4
    items_por_consumidor = num_productores * items_por_productor // num_consumidores
    
    cinta = CintaTransportadora(capacidad_cinta)
    
    productores = []
    consumidores = []
    
    # Crear productores
    for i in range(num_productores):
        t = threading.Thread(target=productor_multiple, args=(cinta, i, items_por_productor))
        productores.append(t)
    
    # Crear consumidores
    for i in range(num_consumidores):
        t = threading.Thread(target=consumidor_multiple, args=(cinta, i, items_por_consumidor))
        consumidores.append(t)
    
    # Iniciar todos los hilos
    for t in productores + consumidores:
        t.start()
    
    # Esperar a que terminen
    for t in productores + consumidores:
        t.join()
    
    print("Problema de la Cinta Transportadora completado")


class ImpresionAlternada:
    def __init__(self):
        self.turno = 0  # 0: turno del primer proceso, 1: turno del segundo proceso
        self.mutex = threading.Lock()
        self.condicion = threading.Condition(self.mutex)
    
    def imprimir(self, proceso_id, mensaje, num_impresiones):
        for i in range(num_impresiones):
            with self.mutex:
                # Esperar hasta que sea el turno de este proceso
                while self.turno != proceso_id:
                    self.condicion.wait()
                
                # Imprimir mensaje
                print(f"Proceso {proceso_id}: {mensaje} - impresión {i+1}/{num_impresiones}")
                
                # Cambiar turno
                self.turno = 1 - proceso_id
                
                # Notificar al otro proceso
                self.condicion.notify()

def ejecutar_impresion_alternada():
    print("\n--- Ejecutando Problema de Impresión Alternada ---")
    controlador = ImpresionAlternada()
    num_impresiones = 5
    
    # Crear hilos
    proceso0 = threading.Thread(target=controlador.imprimir, args=(0, "Soy el proceso A", num_impresiones))
    proceso1 = threading.Thread(target=controlador.imprimir, args=(1, "Soy el proceso B", num_impresiones))
    
    # Iniciar hilos
    proceso0.start()
    proceso1.start()
    
    # Esperar a que terminen
    proceso0.join()
    proceso1.join()
    
    print("Problema de Impresión Alternada completado")


def main():
    print("SIMULACIÓN DE PROBLEMAS CLÁSICOS DE CONCURRENCIA")
    
    ejecutar_productor_consumidor()
    ejecutar_filosofos_comensales()
    ejecutar_lectores_escritores()
    ejecutar_barbero_dormilon()
    ejecutar_cinta_transportadora()
    ejecutar_impresion_alternada()

    print("\nTodas las simulaciones han sido completadas exitosamente.")

if __name__ == "__main__":
    main()