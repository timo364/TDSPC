from threading import Thread as Trd, Event, Lock


LST = []


class InputThread(Trd):
    '''
    Main thread that reads user input.
    When current thread starts, it's also starting `SortThread`.
    '''
    def __init__(self):
        super().__init__()

        self.is_stopped = Event()
        self.lock = Lock()

    def run(self):
        # Using global variable to demontrate shared data.
        global LST

        # Starting SortThread(), that safely sorts global list every 30 seconds.
        self.sort_trd = SortThread(self.lock)
        self.sort_trd.start()

        # If user enters an empty string, all threads will be stopped.
        while not self.is_stopped.is_set():
            user_input = input('Enter your number value(s).\nTo stop, enter empty string.\n')

            if user_input == '':
                # Trying to access shared data safely.
                # If self.lock is acquired == True, waiting for releasing.
                with self.lock:
                    # Then, printing sorted data and stopping.
                    print(f'{LST}\n')
                    self.sort_trd.get_event_of_this_thread().set()
                    self.is_stopped.set()
            else:
                # Appending user input if its has number type only.
                try:
                    LST.append(int(user_input))
                except ValueError:
                    print('Error: you can enter only int values.\n')


class SortThread(Trd):
    '''
    Thread for sorting shared data.
    Sorts all data in global variable `LST` for every 30 seconds until the main
    `InputThread` will not stop everyting.
    '''
    def __init__(self, lock:Lock):
        super().__init__()

        self.is_it_time_to_sort = Event()
        self.lock = lock

    def run(self):
        while not self.is_it_time_to_sort.wait(30):
            self.lock.acquire()
            LST.sort()
            self.lock.release()

    def get_event_of_this_thread(self):
        '''
        This getter created for stopping current thread from main, `InputTread`.
        '''
        return self.is_it_time_to_sort


if __name__ == '__main__':
    InputThread().start()

