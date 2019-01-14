import numpy as np
from numpy.lib import recfunctions
import scipy.io as sio

from helpers import list_tools
from helpers import uid_tools
from helpers import time_tracker

from data_classes import DataFile, Dataset
from datetime import datetime


def load_file(file, dataset_selection=None, print_progress=False):

    tt = time_tracker.TimeTracker(print_process=print_progress)

    start_time = datetime.now()
    print('\nLoading file %s... ' % file)

    tt.tic()
    raw_data = sio.loadmat(file)
    tt.toc('loadmat')

    # Determine number of messages
    n_messages = raw_data['messages'].shape[1]
    tt.toc('determine n_messages')

    # Get IDs from the raw data
    message_ids = np.reshape(np.transpose(raw_data['messages'][0:2, :]), 2*n_messages)
    # Convert from uint8 to uint16 to obtain IDs
    message_ids.dtype = np.uint16
    tt.toc('get message IDs')

    # Get timestamps from the raw data
    message_dt = np.reshape(np.transpose(raw_data['messages'][2:4, :]), 2*n_messages)
    message_dt.dtype = np.int16
    # Convert from dt values to absolute timestamps
    message_timestamps = 0.001*np.cumsum(message_dt)
    tt.toc('get timestamps')

    # Filter datasets with plot-able datatypes
    datasets = raw_data['datasets'][raw_data['datasets']['datatype'] <= 9]
    n_datasets = datasets.shape[0]
    if print_progress:
        print('%s plotable datasets found' % n_datasets)
    tt.toc('filter plotable datasets')

    # Run through the dataset and convert 1x1 numpy arrays to normal datatypes
    for field in datasets.dtype.names:
        for i in range(len(datasets[field])):
            datasets[field][i] = list_tools.simplify_list(datasets[field][i])
    tt.toc('convert 1x1 arrays')

    # Check whether UIDs are already present in dataset. If not, generate them
    if 'uid' not in datasets.dtype.names:
        if print_progress:
            print('No UID found. Performing look-up')

        # Generate UID list with generator expression using encoding function of uid_tools
        uids = np.fromiter((uid_tools.encode(datasets['name'][i]) for i in range(datasets.shape[0])), dtype=np.uint32)

        # Append UID field to existing datasets structured array
        datasets = recfunctions.append_fields(datasets, 'uid', uids)
        tt.toc('append UID field')

    # If a dataset_selection is given, only select these
    if dataset_selection:
        pass
        tt.toc('filter out selected datasets')

    # Group messages per dataset
    datasets_to_keep = np.zeros((n_datasets, 1), dtype=np.bool_)
    messages_per_dataset = np.zeros((n_datasets, 1), dtype=np.uint16)
    for i in range(n_datasets):
        # Count number of messages in dataset
        non_zero_messages = np.count_nonzero(message_ids == datasets[i]['id'])

        # This dataset has at least 1 message, so we keep it and save number of messages
        if non_zero_messages > 0:
            datasets_to_keep[i] = True
            messages_per_dataset[i] = non_zero_messages

    # Remove datasets without any messages
    datasets = datasets[np.squeeze(datasets_to_keep)]
    messages_per_dataset = messages_per_dataset[datasets_to_keep]
    n_datasets = datasets.shape[0]
    if print_progress:
        print('%s non-empty datasets left' % n_datasets)
    tt.toc('remove empty datasets')

    # Create data vector
    data_dtype = np.dtype({'names': ['source', 'name', 'UID',
                                     'xData', 'xQuantity', 'xUnit',
                                     'yData', 'yQuantity', 'yUnit',
                                     'startTime'],
                           'formats': ['U2', 'U64', 'i4',
                                       np.object_, 'U64', 'U64',
                                       np.object_, 'U64', 'U64',
                                       'f8']})
    data = np.zeros(n_datasets, dtype=data_dtype)
    tt.toc('create data array')

    # Populate data array
    datatype_conversion = {
        1: np.int8,
        2: np.uint16,
        3: np.int16,
        4: np.uint32,
        5: np.int32,
        6: np.uint64,
        7: np.int64,
        8: np.float32,
        9: np.float64
    }

    for i in range(n_datasets):
        data[i]['source'] = 'SD'
        data[i]['name'] = datasets[i]['name']
        data[i]['UID'] = datasets[i]['uid']
        data[i]['xData'] = np.zeros(messages_per_dataset[i], dtype=np.float64)
        data[i]['xQuantity'] = 'time'
        data[i]['xUnit'] = 's'
        data[i]['yData'] = np.zeros(messages_per_dataset[i], dtype=np.float64)
        data[i]['yQuantity'] = datasets[i]['quantity']
        data[i]['yUnit'] = datasets[i]['unit']

        # Populate xData
        message_indices = np.nonzero(message_ids == datasets[i]['id'])[0]
        data[i]['xData'] = message_timestamps[message_indices]

        # Populate yData
        ls_byte = datasets[i]['byte_offset'] + 4  # index where data starts
        ms_byte = ls_byte + datasets[i]['length']  # index where data ends
        raw_ydata = np.squeeze(raw_data['messages'][ls_byte:ms_byte, message_indices])

        # Convert data to the correct datatype
        datatype = datasets[i]['datatype']
        if datatype != 0:
            raw_ydata.dtype = datatype_conversion[datatype]
        data[i]['yData'] = raw_ydata

        # Apply offset and scaling
        data[i]['yData'] = datasets[i]['offset'] + datasets[i]['scale']*data[i]['yData']

        # Make sure yData is correctly shaped as (n,) instead of (1,n)
        if data[i]['yData'].ndim > 1:
            data[i]['yData'] = np.squeeze(np.transpose(data[i]['yData']))

        # Remove duplicates
        data[i]['xData'], unique_indices = np.unique(data[i]['xData'], return_index=True)
        data[i]['yData'] = data[i]['yData'][unique_indices]

    tt.toc('populate datasets')

    # Sort data based on name
    data = data[np.argsort(data[:]['name'])]
    tt.toc('sort data based on name')

    # Create DataFile object to return
    data_file = DataFile(file, raw_data=data)
    tt.toc('create datafile')

    print('finished in %s seconds' % (datetime.now() - start_time).total_seconds())

    return data_file
