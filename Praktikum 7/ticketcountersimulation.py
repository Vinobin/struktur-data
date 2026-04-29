print("ticket counter simulation")
print("\n")

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

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class TicketCounterSimulation:
    def __init__(self):
        self.queue = Queue()

    def arrive(self, person):
        self.queue.enqueue(person)

    def serve(self):
        if not self.queue.isEmpty():
            return self.queue.dequeue()

    def run(self, n):
        print("Menambahkan pelanggan ke antrian...")
        for i in range(1, n + 1):
            self.arrive(f"Pelanggan-{i}")

        print("Isi antrian:", self.queue)

        print("\nMelayani pelanggan...")
        while not self.queue.isEmpty():
            served = self.serve()
            print("Melayani:", served)

        print("\nAntrian kosong:", self.queue)

if __name__ == "__main__":
    sim = TicketCounterSimulation()
    sim.run(5)