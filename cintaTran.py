import threading
import queue
import time
import random

class CintaTransportadora:
    def __init__(self, buffer_size=5):
        self.buffer = queue.Queue(buffer_size)

    def productor(self, id):
        for _ in range(5):
            item = random.randint(1, 100)
            self.buffer.put(item)
            print(f"Productor {id} produjo: {item}")
            time.sleep(random.uniform(0.1, 0.5))

    def consumidor(self, id):
        for _ in range(5):
            item = self.buffer.get()
            print(f"Consumidor {id} consumió: {item}")
            time.sleep(random.uniform(0.1, 0.5))

if __name__ == "__main__":
    ct = CintaTransportadora()
    for i in range(3):
        threading.Thread(target=ct.productor, args=(i,)).start()
    for i in range(3):
        threading.Thread(target=ct.consumidor, args=(i,)).start()
        