import numpy as np
from numpy.lib import recfunctions
import scipy.io as sio
import time

def sequence_intcanlog(file, dataset_selection=None, track_time=False):
    print('\n Generating sequence from %s' % file)

    # Load data from mat file
    raw_data = sio.loadmat(file)
    messages = raw_data['messages']

    # Determine number of messages
    n_messages = messages.shape[1]
    print('number of messages: %s' % n_messages)

    # Get timestamps from the raw data
    message_dt = np.reshape(np.transpose(messages[2:4, :]), 2*n_messages)
    message_dt.dtype = np.int16
    # Convert from dt values to absolute timestamps
    message_timestamps = 0.001*np.cumsum(message_dt)
    print('duration of file: %i seconds'%(message_timestamps[-1]))

    # Create array to track which messages have been sent
    message_sent = np.zeros(n_messages, dtype=np.bool)

    # Start loop to output data
    start_t = time.time()
    while message_sent.all() != True:
        current_t = time.time() - start_t

        # First determine which indices are in the past
        past = np.where(message_timestamps < current_t)
        # Then determine which indices are not sent yet
        to_be_sent = np.where(message_sent == False)
        # Lastly, intersect these indices to find the message which are both in the past and not send yet
        send_now = np.intersect1d(past, to_be_sent)

        send_messages(send_now)

        # Set sent flag to True for messages which were just sent
        message_sent[send_now] = True

        # Limit data-rate
        time.sleep(0.1)

def send_messages(messages):
    # Send messages to destination
    print('sending %s messages' % messages.shape)
