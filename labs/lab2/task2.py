from threading import Thread as Trd
from queue import SimpleQueue
from time import sleep


class BuildWiget(Trd):
    '''
    This class simulates the operation of a production line.
    First thing first, it builds three details for widget: module which builds
    details A and B, and then builds the last detail C.
    '''

    def __init__(self):
        super().__init__()

        # Using SimpleQueue for demonstrating the imitation of a production line.
        self.queue = SimpleQueue()

    def run(self):
        # Starting build.
        self.__build_widget()

        if self.queue.empty():
            print('Queue is empty! Exiting...')
            return

        # After building, getting all details.
        while not self.queue.empty():
            item = self.queue.get()
            print(f'Got {item}!')

        print('Widget is done! Exiting...')

    def __build_module(self):
        '''Builds the module with two details for wiget: A and B.'''

        print('Building detail A...')
        sleep(1)
        self.queue.put('Detail A')
        print('Detail A: done.\n')

        print('Building detail B...')
        sleep(2)
        self.queue.put('Detail B')
        print('Detail B: done.\n')

    def __build_detail_C(self):
        '''Builds the last detail for wiget: C.'''

        print('Building detail C...')
        sleep(3)
        self.queue.put('Detail C')
        print('Detail C: done.\n')

    def __build_widget(self):
        '''Starts the actual building of widgets.'''

        self.__build_module()
        self.__build_detail_C()


if __name__ == '__main__':
    BuildWiget().start()
