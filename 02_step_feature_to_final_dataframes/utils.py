import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

template_seq = 'AATGATACGGCGACCACCGAGAT' \
               'CTACACGTTCAGAGTTCTACAGT' \
               'CCGACGATCATGGCAACATATTA' \
               'ACGGCATGATATTGACTTATTGA' \
               'ATAAAATTGGGTAAATTtgactcA'\
               'acgatgggttaaNNNNNNNgttGT' \
               'GGTAGTGAGATGAAAAGAGGCGGCG' \
               'cctgcaggNNNNNNNNNNNNNNNTG' \
               'GAATTCTCGGGTGCCAAGGAACTCCA' \
               'GTCACATCACGATCTCGTATGCCGTCT' \
               'TCTGCTTG'
template_seq.upper()


def rc(seq):
    """
    Function to compute the reverse complement of a sequence.
    """
    complement = str.maketrans('ATCGN', 'TAGCN')
    return seq.upper().translate(complement)[::-1]


def read_feature_df(filename):
    """
    Reads a features file; returns as dataframe; prints user feedback.
    """
    print(' ')
    print(f'reading {filename} file ...')
    fname = './pipeline_data/features_combined_' + str(filename) + '.txt'
    df = pd.read_csv(fname, sep='\t')
    print(f'{filename} has {len(df):,} reads')
    print(f'{filename} has {df.columns.values} columns')

    return df


def read_grouped_df(filename):
    """
    Reads a grouped features file; returns as dataframe; prints user feedback.
    """
    print(' ')
    print(f'reading grouped_{filename} file ...')
    fname = './grouped_filter_data/group_' + str(filename) + '.csv.gz'
    df = pd.read_csv(fname)
    print(f'{filename} has {len(df):,} rows')
    print(f'{filename} has {df.columns.values} columns')
    print(' ')

    return df


def read_merged_df(filename):
    """
    Reads merged features file and returns dataframe; prints user feedback.
    """
    print(' ')
    print(f'reading merged_{filename} merged file ...')
    fname = './merged_samp_temp_data/' + str(
        filename) + '_template_merged.csv.gz'
    df = pd.read_csv(fname)
    print(f'{filename} has {len(df):,} rows')
    print(f'{filename} has {df.columns.values} columns')
    print(' ')

    return df

def read_xlink_raw(filename):
    print(' ')
    print(f'reading xlink raw for {filename} ...')
    fname = './xlink_raw_data/features_var_' + str(filename) + '.txt'
    df = pd.read_csv(fname, sep='\t')
    print(f'{filename} has {len(df):,} reads')
    print(f'{filename} has {df.columns.values} columns')

    return df

def x_to_ohe(x):
    """
    Returns:
        The one hot encoded of the sequences.
    """
    alphabet = ['A', 'C', 'G', 'T']
    # Get dimensions
    L = len(x[0])
    N = len(x)
    C = len(alphabet)

    # Shape sequences as array of int8s
    x_arr = np.frombuffer(bytes(''.join(x), 'utf-8'),
                          np.int8, N * L).reshape([N, L])

    # Create alphabet as array of int8s
    alphabet_arr = np.frombuffer(bytes(''.join(alphabet), 'utf-8'),
                                 np.int8, C)

    # Compute (N,L,C) grid of one-hot encoded values
    x_nlc = (x_arr[:, :, np.newaxis] ==
             alphabet_arr[np.newaxis, np.newaxis, :]).astype(np.int8)
    x_ohe = x_nlc.reshape([N, L * C])
    
    return x_ohe