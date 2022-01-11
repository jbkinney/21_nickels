# Processing the fastq files

This folder includes the scripts for our in-house pipeline to process the raw fastq files from the sequencing machine for experiments conducted for the current manuscript.


- Scripts provides in this directory were configured specifically for the Elzar cluster at CSHL, and will likely have to be modified before it is run on a different cluster. 

## Structure of the directory

```
├── 2022_xact_seq_pipeline
│   ├── metadata.xlsx
│   └── params.py
├── README.md
├── run_pipeline.py
└── src
└── fastq
```

- The core of the pipeline are located in `src` [directory](./01_step_fastq_to_feature/src). The content of this folder may not be modified, unless someone need to adopt submitting jobs to other clusters or need to add extra feature extraction.
- The sequencing data (fastq) files from SRA BioProject number **XXXXXX** need to be downloaded and put in `fastq` [directory](./01_step_fastq_to_feature/fastq`).
    - Since the size of fastq data are huge, they are not provided in this repository.
- The pipeline input files are located in `2022_xact_seq_pipeline` [directory](01_step_fastq_to_feature/2022_xact_seq_pipeline). Contents of this folder are:
    - `metadata.xlsx`: This file includes several sheets which point towards each samples fastq file and uses regular expressions to extract the features we are interested from the sequence files.
    - `params.py`: The user-input parameters file. In this file one needs to
        - provide the directory which fastq files are located. By default: `illumina_run_dir = '../fastq'`
        - name of the temporary directory which the bash scripts which submit the computational task on nodes will be saved. We used the UGE system (`qsub`) for submitting tasks on Elzar cluster. By default `tmp_dir = 'tmp'`.
        - name of the intermediate directory which fastq files are split to run on the several computational nodes. In addition the feature files for each split file will be saved here. After, the pipeline finished, this intermediate directory can be removed. By default `interm_dir = 'intermediate'`.
        - Number of sequences which passed to each computational node to be parsed out. Here we split the fastq files by 1,000,000 records. `reads_per_split = int(1E6)`.
        - additional flags for controlling the running jobs:

            ```
            clean_intermediate = True
            make_split_files = True
            make_features_files = True
            merge_feature = True
            clean_tmp = True
            use_cluster = True
            ```

- To run the script:
    - `python run_pipeline.py folder`
    - `folder` is the name of the directory which the parameters (`params.py`) and metadata (`metadata.xlsx)` files are located. In this case to run the script, one should execute `python run_pipeline.py 2022_xact_seq_pipeline`.