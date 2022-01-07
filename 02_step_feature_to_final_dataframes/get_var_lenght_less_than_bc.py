from utils import *
"""
Process sample files
- Read feature files with different var length..
python group_filter_samples.py -S CP49 
"""


def var_len_count(args):
    fname = args.sample_name
    l = args.max_len
    sys.stdout = open(f'./reports/{fname}_var_len_report.txt', 'w')
    df = read_xlink_raw(fname)
    del df['sample']
    print(f'Dropping UMI contains N')
    cond = df.umi.str.contains('N')
    df = df[~cond]
    print('Calculate the var_length')
    df['var_length'] = df['var'].str.len()
    df.reset_index(inplace=True, drop=True)
    df_xlink = df[(df['var_length'] == l)].copy()
    print(f'Counting unique var and umi in {fname} ...')
    n = len(df_xlink)
    print(f'Number of var seq with var_len={l} for {fname} is {n:,}')
    print('')
    print(f'saving the var_length={l} for {fname} in xlink_data')
    df_xlink.reset_index(inplace=True, drop=True)
    df_xlink.to_csv(f'xlink_data/xlink_{fname}.csv.gz',
                    index=False,
                    compression='gzip')
    sys.stdout.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processing sample file")
    parser.add_argument("-s", "--sample_name", type=str)
    parser.add_argument("-l", "--max_len", type=int, default=14)
    args = parser.parse_args()
    var_len_count(args)
