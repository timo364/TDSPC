# Recursive multi-threaded processing of text files.

from threading import Thread
from time import sleep
from os import scandir


def calculate_result_and_write_out(file):
    '''
    Reads file from arg, replaces space between numbers with symbol from first
    line of it, and calculates the result.
    Writes last one to a file called "out.txt".
    '''
    with open(file) as file_read:
        lines = file_read.readlines()
        result = lines[1].replace(' ', lines[0][0])

        with open('out.txt', 'a') as file_write:
            file_write.write(f'{result} = {eval(result)}\n')


if __name__ == '__main__':
    # Clearing file out.txt at startup.
    with open('out.txt', 'w') as file_write:
        file_write.flush()

    for i, file in enumerate(scandir()):
        if file.name == f'in_{i+1}.txt':
            # Specyfing target and passing args to it while initializing Thread.
            Thread(target=calculate_result_and_write_out, args=(file,)).start()
            sleep(0.3)
