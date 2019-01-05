from parsers import intcanlog


class DataStore:
    def __init__(self, inspector):
        self.inspector = inspector
        self.inspector.add('datastore', self)

        self.imported_files = {}

    def load_file(self, filename, track_time = False):
        if filename in self.imported_files:
            print('Warning: overwriting %s' % filename)
        data = intcanlog.load_file(filename, track_time)
        self.imported_files[filename] = data
        self.inspector.get('tree_view').update()

    def unload_file(self, filename):
        try:
            del self.imported_files[filename]
            self.inspector.get('file_browser').update_tree()
        except Exception as e:
            print('Failed unloading file %s: %s'%(filename, e))

    def get_file(self, filename):
        if self.imported_files[filename]: return self.imported_files[filename]
        else:
            raise IndexError('Requested filename not in datastore')

    def get_all_files(self):
        return self.imported_files
