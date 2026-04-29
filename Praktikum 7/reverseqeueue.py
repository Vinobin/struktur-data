

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


def reverseQueue(queue):
    stack = []

  
    while not queue.isEmpty():
        stack.append(queue.dequeue())

    while stack:
        queue.enqueue(stack.pop())

if __name__ == "__main__":
    print("="*40)
    print("        NOMOR 6: REVERSE QUEUE")
    print("="*40)

    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(4)
    q.enqueue(5)

    print("\nQueue awal       :", q)

    reverseQueue(q)

    print("Queue setelah dibalik :", q)