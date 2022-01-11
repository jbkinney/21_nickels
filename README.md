# Analysis code and summary data

**Structural and mechanistic basis of σ-dependent transcriptional pausing**

The computational pipeline used in this study was split into three steps. 
The first two steps run on the Elzar High Performance Computing Cluster at Cold Spring Harbor Laboratory (CSHL). 
The third (final step) is used to plot sequence logos and count profiles presented in the manuscript main text and supplements. The detailed descriptions of the three steps mentioned bellow are in separate README files in each folder.

## Step 1: [Processing the fastq files](./01_step_fastq_to_feature) 
- The scripts for running this step are provided in `01_step_fastq_to_feature` [directory](./01_step_fastq_to_feature).
- We explained how to run this step in the (README)[01_step_fastq_to_feature/README.md] file.
- One need to download all sequencing data (fastq) files from SRA BioProject number **XXXXXX** and deposit into the
`./01_step_fastq_to_feature/fastq` directory.
- We provided the metadata file `01_step_fastq_to_feature/metadata.xlsx` in which the name of samples should match the fastq files.
- We called the output of this step **feature** files which are needed for the Step 2. 

## Step 2: [Processing the feature files](./02_step_feature_to_final_dataframes) 

- The scripts for running this step are provided in `02_step_feature_to_final_dataframe` [directory](./02_step_feature_to_final_dataframes). 
- The step-by-step guideline for this step is provided in the [README](02_step_feature_to_final_dataframes/README.md) file.
- The features files from Step 1 are further processed to get 
    
    - Raw pause elements, A-site dataframes for each replicates in the [pe_aloc_directory](./02_step_feature_to_final_dataframes/pe_aloc_pairs_data).    
    - Template, ligation and cross-link bias corrected pause elements and A-site counts as well as global logos for each replicate [2022_XACT_seq_data](./02_step_feature_to_final_dataframes/2022_XACT_seq_data).
    - As disscused in the manuscript, for ligation and cross-link corrections we used the data from the following paper which we refer it as *XACT_seq (2020)* here.
    [Winkelman, Jared T., et al. "XACT-seq comprehensively defines the promoter-position and promoter-sequence determinants for initial-transcription pausing." Molecular cell 79.5 (2020): 797-811](https://doi.org/10.1016/j.molcel.2020.07.006). The dataframe which is used for ligation and cross-link corrections from XACT_seq (2020) is also provided in
    [xlink_lig_ave_xact_seq.csv.gz](./02_step_feature_to_final_dataframes/xact_seq_bias_data/xlink_lig_ave_xact_seq.csv.gz) for convenience.  
   
## Step 3: [Making sequence logos and count profiles](./02_step_feature_to_final_dataframes) 
- The separate [README](03_step_final_dataframe_to_logos/README.md) file is provided for detailed description of this step.
- The content of this folder is standalone and one should be easily able to reproduce all the sequence logos and count profiles.
- The scripts in this step depend on popular scientific python packages like `numpy, pandas` and `matplotlib`. In addition, for sequence logos we used the Python package [logomaker](https://logomaker.readthedocs.io/en/latest/).
- The scripts are in the form of `jupyter-notebook` files as follows:
    - [`2014_Vvedenskaya_figs.ipynb`](03_step_final_dataframe_to_logos/2014_Vvedenskaya_sites/2014_Vvedenskaya_figs.ipynb): Sequence logo for [Vvedenskaya, Irina O., et al. "Interactions between RNA polymerase and the “core recognition element” counteract pausing." Science 344.6189 (2014): 1285-1289](https://doi.org/10.1126/science.1253458) paper.
    - [`2020_XACT_seq_logos_figs.ipynb`](03_step_final_dataframe_to_logos/2020_XACT_seq/2020_XACT_seq_logos_figs.ipynb): Sequence logos for the XACT_seq (2020) paper.
    - [`2022_XACT_seq_logos_figs.ipynb`](03_step_final_dataframe_to_logos/2022_XACT_seq/2022_XACT_seq_logos_figs.ipynb): Sequence logos and count profiles for the experiments conducted for the current manuscript.