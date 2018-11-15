from parsers.intcanlog import *
import numpy as np

class DataStore:
    def __init__(self):
        print('Data Store initialized')
        self.imported_files = []

    def load_file(self, file, track_time=False):
        self.imported_files.append(load_intcanlog(file, track_time=track_time))
