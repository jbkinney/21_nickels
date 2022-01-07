from utils import *
"""
Counting the (pe, var) pairs.
"""


def count_pe_vars(args):
    fname = args.sample_name
    sys.stdout = open(f'./reports/{fname}_pe_aloc_count_report.txt', 'w')
    df = read_merged_df(fname)
    print('Drop var, and count_template ...')
    print('Drop possible duplicates ... ')
    del df['var']
    del df['count_template']
    print('Replace var_length with a_loc ...')
    df['a_loc'] = 54 - df['var_length']
    del df['var_length']
    df.reset_index(inplace=True, drop=True)
    df['count'] = 1
    count_df = df.groupby(['pe', 'a_loc']).sum()
    count_df.reset_index(inplace=True)
    print(' ')
    n = len(count_df)
    print(f'Total rows of pe aloc pairs are {n:,}')
    print(' ')
    print(
        f'writing the pe aloc count for {fname} in pe_aloc_pairs_data folder')
    count_df.to_csv(f'pe_aloc_pairs_data/{fname}_pe_aloc.csv.gz', index=False)
    sys.stdout.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processing the merged files")
    parser.add_argument("-s", "--sample_name", type=str)
    args = parser.parse_args()
    count_pe_vars(args)
