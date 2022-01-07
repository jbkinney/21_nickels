# Analysis code and summary data

**Structural and mechanistic basis of σ-dependent transcriptional pausing**

The computational pipeline used in this study was split into three steps: 

1. Step 1: `01_step_fastq_to_feature`: 

    - This component run on the `Elzar` High Performance Computing Cluster at Cold Spring Harbor Laboratory (CSHL). 

    - Scripts provides in this directory was configured specifically for the `Elzar` cluster at CSHL, and will likely have to be modified before it is run on a different cluster. 
    - To run this pipeline, first we need all `fastq` sequencing data and deposit them into the directory `/01_step_fastq_to_feature/fastq` directory. 
    - The name of the `fastq` files should be matched with the `01_step_fastq_to_feature/var_seq/090821_xactseq.xlsx` metadate file.
    - To run the pipeline one can execute `python run_pipeline.py var_seq`.
    - The output of this step is called `feature` files which are explained in details in the `Step 2`. 

2. Step 2: `02_step_feature_to_final_dataframes`:

    - The scripts provided for the second step run on the `Elzar` High Performance Computing Cluster at Cold Spring Harbor Laboratory (CSHL). However, any machine with adequate computational resources would be able to run them.

    - We added the step-by-step guideline in the README file inside the directory.

    - The input of this step are those `feature` files from Step 1. In addition, for ligation and cross-link bias correction one need to provide the appropriate data from analysis of the XACT_seq (2020) paper refereed below. For convenience, the dataframe used for bias correction from XACT_seq (2020) is provided. 
    
    [Winkelman, Jared T., et al. "XACT-seq comprehensively defines the promoter-position and promoter-sequence determinants for initial-transcription pausing." Molecular cell 79.5 (2020): 797-811.](https://doi.org/10.1016/j.molcel.2020.07.006)
   
    - Outputs of this step are:
        - Template, ligation and crosslink bias corrected pause elements and A-site for each replicate.
        - Global sequence logos for each replicate.
        - Rescaled values for count after bias corrections for each replicates.
        - Raw pause elements, A-site dataframes for each replicates.

    - In addition to the step-by-step instruction in the README file, one would get the full details of template, ligation and crosslink corrections from the manuscript.

 3. Step 3: `03_step_final_dataframe_to_logos`
 
    - Scripts provided in this step plot logos for current experiments, as well as XACT_seq (2020) experiments. 
    - The content of this folder is standalone and one should be easily reproduce all the sequence logos. 
    - Note that scripts depend on popular scientific python packages like `numpy, pandas` and `matplotlib`. In addition, for sequence logos we used the Python package [logomaker](https://logomaker.readthedocs.io/en/latest/)
    - Scripts are provided in the form of `jupyter-notebook`s.