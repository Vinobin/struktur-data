import random

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop(0)


class TicketCounterSimulation:
    def __init__(self):
        self.queue = Queue()
        self.current_time = 0
        self.wait_times = []

    def arrive(self, arrival_time):
        self.queue.enqueue(arrival_time)

    def serve(self, service_time):
        if not self.queue.isEmpty():
            arrival_time = self.queue.dequeue()
            wait_time = self.current_time - arrival_time
            if wait_time < 0:
                wait_time = 0
            self.wait_times.append(wait_time)
            self.current_time += service_time

    def run(self, num_customers):
        for _ in range(num_customers):
            arrival_time = random.randint(1, 5) * 60
            self.arrive(arrival_time)
        while not self.queue.isEmpty():
            service_time = random.randint(1, 3) * 60
            self.serve(service_time)
        if len(self.wait_times) > 0:
            return sum(self.wait_times) / len(self.wait_times)
        return 0


if __name__ == "__main__":
    print("="*50)
    print("   NOMOR 5: SIMULASI (SATUAN DETIK)")
    print("="*50)
    print("\nJumlah Pelanggan | Rata-rata Waktu Tunggu (detik)")
    print("--------------------------------------------------")
    for customers in [10, 20, 30]:
        sim = TicketCounterSimulation()
        avg_wait = sim.run(customers)
        print(f"{customers:<17} | {round(avg_wait, 2)}")