import threading
import queue
import time
import random

class ProductorConsumidor:
    def __init__(self, buffer_size=5):
        self.buffer = queue.Queue(buffer_size)
        self.lock = threading.Lock()

    def productor(self):
        for _ in range(10):
            item = random.randint(1, 100)
            self.buffer.put(item)
            print(f"Productor produjo: {item}")
            time.sleep(random.uniform(0.1, 0.5))

    def consumidor(self):
        for _ in range(10):
            item = self.buffer.get()
            print(f"Consumidor consumió: {item}")
            time.sleep(random.uniform(0.1, 0.5))

if __name__ == "__main__":
    pc = ProductorConsumidor()
    threading.Thread(target=pc.productor).start()
    threading.Thread(target=pc.consumidor).start()
    