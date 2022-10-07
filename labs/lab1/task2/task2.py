from threading import Thread
import numpy as np
from time import sleep


class CustomThread(Thread):
    def __init__(self, m, n, k):
        super().__init__()
        self.m = m
        self.n = n
        self.k = k

    def run(self):
        arr1 = np.random.randint(
            self.m + self.n, size=(self.m, self.n))
        arr2 = np.random.randint(
            self.n + self.k, size=(self.n, self.k))
        mul = arr1.dot(arr2)

        print(f"{self.name}:\n{mul}")
        sleep(1)
        print(f"{self.name} finished.")


if __name__ == '__main__':
    p = 4
    for i in range(p):
        CustomThread(2, 3, 4).start()
        sleep(0.5)
