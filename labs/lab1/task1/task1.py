from threading import Thread
from time import sleep
from random import randint


class CustomThread(Thread):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        print(f'Printing some value: {self.text} ' + str(randint(1, 10)))
        sleep(1)
        print(f'{self.name} finished.')


if __name__ == '__main__':
    for i in range(4):
        # Creating custom thread instance, running and sleeping specifying target and passing arg to target func.
        trd = CustomThread('Hello, World!').start()
        sleep(0.5)
