import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logomaker

# Read the template feature file
template_df = pd.read_csv('./pipeline_data/features_combined_template.txt',
                          delim_whitespace=True)
del template_df['var_length']
# Alignment of the template dataframe
template_alignment_mat = logomaker.alignment_to_matrix(
    template_df['pe'].values)

# Construct the background and foregroind
fg_df_prob_template = logomaker.transform_matrix(template_alignment_mat[['A', 'C', 'G', 'T']],
                                                 from_type='counts',
                                                 to_type='probability')

bg_df_prob_template = pd.DataFrame(0.25*np.ones(shape=fg_df_prob_template.shape),
                                   columns=['A', 'C', 'G', 'T'])


# Compute the enrichement for template
template_weight_df = np.log2(fg_df_prob_template/bg_df_prob_template)

# Save the template weights to the pe_aloc_pairs folder
template_weight_df.to_csv('./2022_XACT_seq_data/template_weight_sigma_df.csv.gz',
                          compression='gzip', index=False)
