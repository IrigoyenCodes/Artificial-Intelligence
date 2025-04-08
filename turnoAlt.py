import threading
import time

class TurnoAlternado:
    def __init__(self):
        self.turno = threading.Semaphore(1)

    def proceso_a(self):
        for _ in range(5):
            self.turno.acquire()
            print("Proceso A ejecutando.")
            time.sleep(1)
            self.turno.release()

    def proceso_b(self):
        for _ in range(5):
            self.turno.acquire()
            print("Proceso B ejecutando.")
            time.sleep(1)
            self.turno.release()

if __name__ == "__main__":
    ta = TurnoAlternado()
    threading.Thread(target=ta.proceso_a).start()
    threading.Thread(target=ta.proceso_b).start()