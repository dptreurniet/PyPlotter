class DataFile:
    def __init__(self, filename, raw_data=None):
        self.filename= filename.split('/')[-1]
        self.datasets = []

        if type(raw_data) != None:
            for data in raw_data:
                self.datasets.append(Dataset(data))


    def append_dataset(self, dataset):
        self.datasets.append(dataset)

    def get_names(self):
        names = []
        for dataset in self.datasets:
            names.append(dataset.get_name())
        return names

    def get_uids(self):
        uids = []
        for dataset in self.datasets:
            uids.append(dataset.get_uid())
        return uids

    def get_filename(self): return self.filename

    def get_datasets(self):
        return self.datasets

    def get_dataset_by_name(self, name):
        for dataset in self.datasets:
            if dataset.get_name() == name:
                return dataset
        return None

    def get_dataset_by_uid(self, uid):
        for dataset in self.datasets:
            if dataset.get_uid() == uid:
                return dataset
        return None



class Dataset:
    def __init__(self, raw):
        self.source = raw['source']
        self.name = raw['name']
        self.UID = raw['UID']
        self.xData = raw['xData']
        self.xQuantity = raw['xQuantity']
        self.xUnit = raw['xUnit']
        self.yData = raw['yData']
        self.yQuantity = raw['yQuantity']
        self.yUnit = raw['yUnit']

    def get_name(self): return self.name

    def get_uid(self): return self.UID
