import time
import numpy as np

class TimeTracker:
    def __init__(self, print_process):
        self.print_process = print_process
        self.start_time = time.time()
        self.end_time = time.time()

    def tic(self):
        self.start_time = time.time()

    def toc(self):
        self.toc('')

    def toc(self, process, tic=True):
        self.end_time = time.time()
        if self.print_process:
            print('--- %s: %0.3f sec' % (process, self.end_time - self.start_time))
        if tic:
            self.tic()

def simplify_list(lst):
    """
    Recursive function to simplify a nested list to the most basic form.
    The nested list can have unknown depth and unknown content.
    In case of a single value, it will return a single value.
    In case of a list with more values, it will return a simple list.

    :param lst: list to simplify
    :return: lowest level object
    """
    list_obj = [list, np.ndarray]

    # Check if current lst is a list or array. If not, return it
    if type(lst) not in list_obj:
        return lst
    # lst is a list, so check if there is something in it. If not, return None
    elif lst.size == 0:
        return None
    # lst is a list with something in it. Go down recursively
    else:
        return simplify_list(lst[0])
