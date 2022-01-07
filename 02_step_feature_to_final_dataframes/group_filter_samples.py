from utils import *
"""
Process sample files
- Read fastq file from samples.
- Groping the (umi, bc) with highest mode.
- Write the report.
- For example:
python group_filter_samples.py -S CP49 
"""

def sample_file_process(fname):
    sys.stdout = open(f'./reports/{fname}_group_filter_report.txt', 'w')

    df = read_feature_df(fname)
    del df['sample']
    print(f'Dropping BC and UMI contains N')
    cond = df.bc.str.contains('N')
    df = df[~cond]
    cond = df.umi.str.contains('N')
    df = df[~cond]
    df.reset_index(inplace=True, drop=True)
    print(f'Counting unique bc and umi in {fname} ...')
    n = np.unique(df['bc']).shape[0]
    m = np.unique(df['umi']).shape[0]
    print(f'Number of unique bc in {fname} are {n:,}')
    print(f'Number of unique umi in {fname} are {m:,}')
    print('')
    # Select the (umi, bc) pairs with highest mode)
    mode = lambda x: x.mode() if len(x) > 2 else min(x)
    print(f'Grouping umi and bc for {fname} sample with highest modes ...')
    umi_bc_df = df.groupby(['umi','bc']).agg(mode).reset_index()
    print(f'Get rid of rows with two vars sequences ...')
    print(' ')
    cond = umi_bc_df['var'].str.contains(']', na=True)
    umi_bc_df =umi_bc_df[~cond]
    print(f'Get rid of two var lengths rows ...')
    print(' ')
    cond = umi_bc_df['var_length'].apply(lambda x: ']' in str(x))
    umi_bc_df =umi_bc_df[~cond]
    umi_bc_df.reset_index(inplace=True, drop=True)
    n = len(umi_bc_df)
    print(f'Number of unique (umi, bc) pairs in {fname} is {n:,}')
    print(f'saving the (umi, bc) grouped for {fname} in grouped_filter_data folder')
    umi_bc_df.to_csv(f'grouped_filter_data/group_{fname}.csv.gz', 
        index=False, compression='gzip')
    sys.stdout.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Processing sample file")
    parser.add_argument("-s", "--sample_name", type=str)
    args = parser.parse_args()
    sample_file_process(args.sample_name)
