import threading
import time
import random

class Filosofo(threading.Thread):
    def __init__(self, id, tenedor_izq, tenedor_der):
        super().__init__()
        self.id = id
        self.tenedor_izq = tenedor_izq
        self.tenedor_der = tenedor_der

    def run(self):
        while True:
            print(f"Filósofo {self.id} está pensando.")
            time.sleep(random.uniform(0.5, 1.5))
            self.comer()

    def comer(self):
        with self.tenedor_izq, self.tenedor_der:
            print(f"Filósofo {self.id} está comiendo.")
            time.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    tenedores = [threading.Lock() for _ in range(5)]
    filosofos = [Filosofo(i, tenedores[i], tenedores[(i+1)%5]) for i in range(5)]
    for f in filosofos:
        f.start()