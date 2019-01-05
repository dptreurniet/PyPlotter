import numpy as np


class DataFile:
    def __init__(self, filename, raw_data):
        self.filename= filename.split('/')[-1]
        self.datasets = []

        for dataset_raw in raw_data:
            self.datasets.append(Dataset(dataset_raw))

    def get_titles(self):
        titles = []
        for dataset in self.datasets:
            titles.append(dataset.title)
        return titles

    def get_uids(self):
        UIDs = []
        for dataset in self.datasets:
            UIDs.append(dataset.UID)
        return UIDs

    def get_filename(self): return self.filename

    def get_datasets(self): return self.datasets

    def get_dataset(self, title=None):
        if title:
            for dataset in self.datasets:
                if dataset.title == title: return dataset


class Dataset:
    def __init__(self, raw):
        self.source = raw['source']
        self.title = raw['title']
        self.UID = raw['UID']
        self.xData = raw['xData']
        self.xQuantity = raw['xQuantity']
        self.xUnit = raw['xUnit']
        self.yData = raw['yData']
        self.yQuantity = raw['yQuantity']
        self.yUnit = raw['yUnit']
