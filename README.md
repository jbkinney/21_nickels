# Analysis code and summary data

**Structural and mechanistic basis of σ-dependent transcriptional pausing**

The computational pipeline used in this study was split into three steps. 
The first two steps run on the Elzar High Performance Computing Cluster at Cold Spring Harbor Laboratory (CSHL). 
The third (final step) is used to plot sequence logos and count profiles presented in the manuscript main text and supplements. The detailed descriptions of the three steps mentioned bellow are in separate README files in each folder.

## Step 1: [Processing the fastq files](./01_step_fastq_to_feature) 
- The scripts for running this step are provided in `01_step_fastq_to_feature`. 
- One need to download all sequencing data (fastq) files from SRA BioProject number **XXXXXX** and deposit into the directory
`/01_step_fastq_to_feature/fastq`.
- We provided the metadata file `01_step_fastq_to_feature/metadata.xlsx` in which the name of samples should match the fastq files.
- We called the output of this step **feature** files which are needed for the Step 2. 


## Step 2: [Processing the feature files](./02_step_feature_to_final_dataframes) 
2. Step 2: `02_step_feature_to_final_dataframes`:

    - The scripts provided for the second step run on the `Elzar` High Performance Computing Cluster at Cold Spring Harbor Laboratory (CSHL). However, any machine with adequate computational resources would be able to run them.

    - We added the step-by-step guideline in the README file inside the directory.

    - The input of this step are those `feature` files from Step 1. In addition, for ligation and cross-link bias correction one need to provide the appropriate data from analysis of the XACT_seq (2020) paper refereed below. For convenience, the dataframe used for bias correction from XACT_seq (2020) is provided. **WHICH FILE?**
    
    [Winkelman, Jared T., et al. "XACT-seq comprehensively defines the promoter-position and promoter-sequence determinants for initial-transcription pausing." Molecular cell 79.5 (2020): 797-811.](https://doi.org/10.1016/j.molcel.2020.07.006)
   
    - Outputs of this step are **WHAT ARE THE FILE NAMES?**:
        - Template, ligation and crosslink bias corrected pause elements and A-site for each replicate.
        - Global sequence logos for each replicate.
        - Rescaled values for count after bias corrections for each replicates.
        - Raw pause elements, A-site dataframes for each replicates.

    - In addition to the step-by-step instruction in the README file, one would get the full details of template, ligation and crosslink corrections from the manuscript.

 3. Step 3: `03_step_final_dataframe_to_logos`
 
    - Scripts provided in this step plot logos for current experiments, as well as XACT_seq (2020) experiments. **WHAT ARE THE FILE NAMES? WHICH SCRIPTS DO WHAT?**
    - The content of this folder is standalone and one should be easily reproduce all the sequence logos. 
    - Note that scripts depend on popular scientific python packages like `numpy, pandas` and `matplotlib`. In addition, for sequence logos we used the Python package [logomaker](https://logomaker.readthedocs.io/en/latest/)
    - Scripts are provided in the form of `jupyter-notebook`s.
