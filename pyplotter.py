# Created by Daan Treurniet

from datastore import DataStore
from datagenerator import sequence_intcanlog

data_store = DataStore()

data_store.load_file('data/test_data.mat')
