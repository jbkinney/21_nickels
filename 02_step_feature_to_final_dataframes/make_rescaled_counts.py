from utils import *
import logomaker


def get_pivot_df(fname):
    """
    Returns:
    1. CP_raw_df: sample dataframe with [pe, a_loc, count]
    2. CP_df: sample dataframe pivot with [pe, aloc_0, aloc_1, ...., aloc_n, total]    
    """

    # Read the (pe, aloc, count data)
    CP_raw_df = pd.read_csv(f'./pe_aloc_pairs_data/{fname}_pe_aloc.csv.gz')
    # Pivoting the dataframe
    CP_df = CP_raw_df.pivot(index='pe', columns='a_loc',
                            values='count').fillna(0).copy()
    CP_df.reset_index(inplace=True)
    return CP_raw_df, CP_df


# Get DNA template correction for the 2022 XACT-seq data
# The template sequence for 2022 XACT-seq up to barcode
template_seq = ("AATGATACGGCGACCACCGAGATCTACACGTTCAGAGTTCTACAGT"
                "CCGACGATCATGGCAACATATTAACGGCATGATATTGACTTATTGA"
                "ATAAAATTGGGTAAATTTGACTCAACGATGGGTTAANNNNNNNGTT"
                "GTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG")
print(f'Length of template seq is {len(template_seq)}')

template_weight_df = pd.read_csv(
    './2022_XACT_seq_data/template_weight_sigma_df.csv.gz')

# Read the average biases for crossline and ligation from 2020 XACT-seq data
enrich_mat_xact_ave = pd.read_csv(
    './xact_seq_bias_data/xlink_lig_ave_xact_seq.csv.gz')
enrich_mat_xact_ave.index = enrich_mat_xact_ave.index - 2


for sample_name in ['CP49', 'CP50', 'CP51', 'CP52', 'CP53', 'CP54']:
    a_loc_range = np.arange(10, 22)

    # Get pe, a_loc data for each 2021 sample.
    print(f'> Reading sample {sample_name}')
    CP_raw_df, CP_df = get_pivot_df(sample_name)
    # Number of reads for each xlink_pos
    print(f'   >> Counting Number of reads for each A-sites in {sample_name}')
    num_reads = CP_df.sum(numeric_only=True).to_frame().reset_index()
    num_reads.rename(columns={0: 'reads'}, inplace=True)

    print(f'   >> Correct the 2022 {sample_name} data with 2022 template')
    x_ohe_PE = x_to_ohe(CP_df['pe'].values)
    template_rescaling_factors = 2**(
        np.sum((x_ohe_PE*template_weight_df.values.ravel()), axis=1)).reshape(-1, 1)
    # Template corrected dataframe
    CP_temp_cor_df = CP_df.drop('pe', axis=1).div(template_rescaling_factors)
    CP_temp_cor_df.insert(0, 'pe', CP_df['pe'])

    print(
        f'   >> Rescale 2022 template corrected sample {sample_name} with 2020 xlink and ligation biases')
    # Rescale the template corrected logos with average bias
    CP_df_rescaled = CP_temp_cor_df.copy()
    # Make temporarily one column for sequences with PE inserted
    CP_df_rescaled.insert(0, 'seq_with_pe',
                          template_seq[:128]+CP_df_rescaled['pe']
                          + "GTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG")
    len_seq_with_PE = len(CP_df_rescaled['seq_with_pe'][0])

    for a_loc in CP_df_rescaled.columns[2:]:
        left_site = 128+a_loc-11
        right_site = 128+a_loc-6
        if (left_site < len_seq_with_PE) and (right_site < len_seq_with_PE):
            bias_seq_array = np.empty(shape=CP_df_rescaled['seq_with_pe'].shape,
                                      dtype=object)
            for seq_id, seq in enumerate(CP_df_rescaled['seq_with_pe']):
                bias_sequence_for_a_loc = seq[left_site: right_site]
                bias_seq_array[seq_id] = bias_sequence_for_a_loc
            x_ohe = x_to_ohe(bias_seq_array)
            rescale_factor = 2**(np.sum((x_ohe *
                                 enrich_mat_xact_ave.values.ravel()), axis=1))
            CP_df_rescaled[a_loc] = CP_df_rescaled[a_loc]/rescale_factor
    del CP_df_rescaled['seq_with_pe']
    
    print(f'   >> Save the rescaled dataframe for {sample_name}')

    CP_df_rescaled.to_csv(f'./2022_XACT_seq_data/{sample_name}_rescaled.csv.gz',
                          compression='gzip', index=False)
    
    print(f'   >> Save the rescaled counts {sample_name}')
    num_rescaled_count = CP_df_rescaled.sum(numeric_only=True).to_frame().T
    num_rescaled_count.to_csv(
        f'./2022_XACT_seq_data/rescale_counts_{sample_name}.csv.gz',
        index=False, compression='gzip')

    # Find the global logo for the 4nt in each replicate for +16
    # Create average enrichment array
    print(f'   >> Save global logo dataframe for {sample_name}')
    a_loc = 16
    seqs = CP_df_rescaled['pe']

    nt_cond = [a_loc-2, a_loc-1, a_loc, a_loc+1, a_loc+2, a_loc+3, a_loc+4]
    ct_cols = CP_df_rescaled.columns[1:]
    fg_ct = CP_df_rescaled[a_loc].values
    fg_mat = logomaker.alignment_to_matrix(sequences=seqs,
                                           counts=fg_ct, pseudocount=1)
    enrich_mat = np.log2(fg_mat)
    enrich_mat.index = enrich_mat.index+14
    enrich_mat_sample = enrich_mat.loc[nt_cond].values
    enrich_mat_sample = pd.DataFrame(enrich_mat_sample,
                                     columns=['A', 'C', 'G', 'T'])
    enrich_mat_sample.to_csv(f'./2022_XACT_seq_data/global_logo_{sample_name}.csv.gz',
                             compression='gzip', index=False)
