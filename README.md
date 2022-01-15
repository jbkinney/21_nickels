# Analysis code and summary data

**Structural and mechanistic basis of σ-dependent transcriptional pausing**

The computational pipeline used in this study was split into three steps. 
The first two steps run on the Elzar High Performance Computing Cluster at Cold Spring Harbor Laboratory (CSHL). 
The third (final step) is used to plot sequence logos and count profiles presented in the manuscript main text and supplements. The detailed descriptions of the three steps mentioned bellow are in separate README files in each folder.

## Step 1: [Processing the fastq files](./01_step_fastq_to_feature)

- The scripts for running this step are provided in `01_step_fastq_to_feature` [directory](./01_step_fastq_to_feature).
- We explained how to run this step in the [README](./01_step_fastq_to_feature/README.md) file.
- The inputs of this step is the raw fastq files and the output of this step are called **feature** files. 

## Step 2: [Processing the feature files](./02_step_feature_to_final_dataframes) 

- The scripts for running this step are provided in `02_step_feature_to_final_dataframe` [directory](./02_step_feature_to_final_dataframes). 
- The step-by-step guideline for this step is provided in the [README](02_step_feature_to_final_dataframes/README.md) file.
- The inputs of this step are features files from Step 1 and outputs are `csv` files in the [pe_aloc_pairs](./02_step_feature_to_final_dataframes/pe_aloc_pairs_data) and [2022_XACT_seq_data](./02_step_feature_to_final_dataframes/2022_XACT_seq_data) directory.
   
## Step 3: [Making sequence logos and count profiles](./03_step_final_dataframe_to_logos)

- The scripts for running this step are provided in `03_step_final_dataframe_to_logos` [directory](./03_step_final_dataframe_to_logos). 
- The separate [README](03_step_final_dataframe_to_logos/README.md) file is provided for detailed description of this step.
- The inputs of this steps are the `csv` files from Step 2 and outputs are the sequence logos and rescaled counts figures which some of them are presented in the manuscript.

Please address technical questions about this repository and its contents to [Justin B. Kinney](mailto:jkinney@cshl.edu). More general scientific correspondence about this work should be sent to [Bryce Nickels](mailto:bnickels@waksman.rutgers.edu).
The sequencing data (fastq) files from SRA BioProject number [SRP355098](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP355098).