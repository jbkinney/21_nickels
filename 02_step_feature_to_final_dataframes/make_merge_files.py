from utils import *


def merging_samp_temp(args):
    template_name = args.template_name
    sample_name   = args.sample_name
    sys.stdout = open(f'./reports/{sample_name}_merge_report.txt', 'w')
    
    template_df = read_grouped_df(template_name)
    sample_df   = read_grouped_df(sample_name)
    print(f'Merge {template_name} and {sample_name} on bc ...')
    df = sample_df.merge(template_df,on='bc').copy()
    df.reset_index(inplace=True, drop=True)
    print(' ')
    n = len(df)
    print(f'number of (umi, bc, pe) for {sample_name} merged with {template_name} are {n:,}')
    print(' ')
    print(f'writing the {sample_name}_{template_name}_merge.csv.gz ...')
    df.to_csv(f'merged_samp_temp_data/{sample_name}_{template_name}_merged.csv.gz',
            index=False, compression='gzip')
    sys.stdout.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Processing sample file")
    parser.add_argument("-s", "--sample_name", type=str)
    parser.add_argument("-t", "--template_name", type=str, default='template')
    args = parser.parse_args()

    merging_samp_temp(args)
