import threading
import time
import random

class LectoresEscritores:
    def __init__(self):
        self.mutex = threading.Lock()
        self.escritor = threading.Lock()
        self.lectores = 0

    def leer(self, id):
        with self.mutex:
            self.lectores += 1
            if self.lectores == 1:
                self.escritor.acquire()
        print(f"Lector {id} está leyendo.")
        time.sleep(random.uniform(0.5, 1.5))
        with self.mutex:
            self.lectores -= 1
            if self.lectores == 0:
                self.escritor.release()

    def escribir(self, id):
        with self.escritor:
            print(f"Escritor {id} está escribiendo.")
            time.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    le = LectoresEscritores()
    for i in range(3):
        threading.Thread(target=le.leer, args=(i,)).start()
    for i in range(2):
        threading.Thread(target=le.escribir, args=(i,)).start()