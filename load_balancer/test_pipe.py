import multiprocessing


def f_producer(queue):
    print(f"Process 1 putting data in the queue")

    for i in range(10):
        queue.put(i)


def f_consumer(queue):
    print("Process 2 polling the queue in order to consume the messages")

    while True:
        item = queue.get()

        if item is None:
            break
        print(item)


class A:
    def __init__(self):
        print("Hello from init")


if __name__ == "__main__":
    q = multiprocessing.Queue()

    a = A()

    p1 = multiprocessing.Process(target=f_producer, args=(q,))
    p2 = multiprocessing.Process(target=f_consumer, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
