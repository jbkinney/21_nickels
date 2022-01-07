from utils import *
"""
Process the template file 
- Read the fastq file from the template feature file.
- Grouping the (pe, bc) together
- Write the report in the reports folder.
"""


def template_file_process(args):
    min_ct = args.min_ct
    fname = args.template_name
    sys.stdout = open(f'./reports/{fname}_group_filter_report.txt', 'w')
    template_df = read_feature_df(fname)
    del template_df['var_length']
    del template_df['sample']
    print(f'Dropping bc and pe that contain N')
    cond = template_df.bc.str.contains('N')
    template_df = template_df[~cond]
    cond = template_df.pe.str.contains('N')
    template_df = template_df[~cond]
    template_df.reset_index(inplace=True, drop=True)
    print(f'Counting unique bc and pe in {fname} ... ')
    n = np.unique(template_df['bc']).shape[0]
    m = np.unique(template_df['pe']).shape[0]
    print(f'Number of unique bc in {fname} are {n:,}')
    print(f'Number of unique pe in {fname} are {m:,}')
    print('')
    
    # Group (bc, pe) and count them
    template_df['count_template']=1
    print('Grouping bc and pe in template file ...')
    pe_bc_df = template_df.groupby(['pe','bc']).sum().reset_index().copy()
    n = len(pe_bc_df)
    print(f'Number of unique (bc,pe) pairs in grouped template is {n:,}')
    print('')
    
    print(f'Filtering template to have at least {min_ct} (bc, pe) counts ...')
    pe_bc_filter_df = pe_bc_df[pe_bc_df['count_template']>min_ct].copy()
    n = len(pe_bc_filter_df)
    print(f'Number of unique (bc,pe) pairs in filtered template is {n:,}')
    print('saving the filtered template in grouped_filter_data folder')
    pe_bc_filter_df.reset_index(inplace=True, drop=True)
    pe_bc_filter_df.to_csv(f'grouped_filter_data/group_{fname}.csv.gz', 
            index=False, compression='gzip')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Processing template file")
    parser.add_argument("-t", "--template_name", type=str, default='template')
    parser.add_argument("-m", "--min_ct", type=int, default=5)
    args = parser.parse_args()
    template_file_process(args)
