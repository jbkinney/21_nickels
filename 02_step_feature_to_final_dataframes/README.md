# Features to final dataframes

This folder contains scripts, which run on the `Elzar` High Performance Computing Cluster at Cold Spring Harbor Laboratory (CSHL).
Scripts provided here are for the **second step** in our overall pipeline to get the sequence logos provided in the paper: 

**Structural and mechanistic basis of σ-dependent transcriptional pausing**

Scripts for the [first](../01_step_fastq_to_feature) and [third](../03_step_final_dataframe_to_logos) steps are provided in the root directory.

Note that, due to the size of intermediate files, we are not providing them here. However, the structure of the directory (including empty folders) are given for clarity.

As it discussed in the manuscript, we used the data from the following manuscript to perform the ligation and cross-link correction. The following paper will be referred as **XACT-seq (2020)** in this guideline.

**Winkelman, Jared T., et al. "XACT-seq comprehensively defines the promoter-position and promoter-sequence determinants for initial-transcription pausing." Molecular cell 79.5 (2020): 797-811.**


## Summary of the second step of the pipeline  

**How to run the scripts for the second step**

The input arguments are described in details in the corresponding sections. 
Throughout this guideline `{sample_names}` are `{CP49, CP50, CP51, CP52, CP53, CP54}`.

1. `python group_filter_template.py -t {template_name} -m {min_ct}`
2. `python group_filter_samples.py  -s {sample_names}`. 
3. `python make_merge_files.py  -s {sample_names} -t {template_name}`
4. `python count_pe_aloc_pairs.py -s {sample_names}`
5. `python make_template_weight.py`
6. `python make_rescaled_counts.py`


**Outputs of the second step**

1. raw pause-element, A-site locations in `./pe_aloc_pairs_data` [directory](../02_step_feature_to_final_dataframes/pe_aloc_pairs_data). The files are saved in `{sample_names}_pe_aloc_csv.gz` format.

2. `./2022_XACT_seq_data` [directory](../02_step_feature_to_final_dataframes/2022_XACT_seq_data):

    - weights for correcting the template bias: [template_weight_sigma_df.csv.gz](../02_step_feature_to_final_dataframes/2022_XACT_seq_data/template_weight_sigma_df.csv.gz).

    - samples corrected by (a) the template from 2022 experiment and (b) by ligation and cross-link biases from XACT-seq (2020) experiment: `{sample_names}_rescaled.csv.gz` in the [directory](../02_step_feature_to_final_dataframes/2022_XACT_seq_data).
    - rescaled counts for each sample: `rescale_{sample_names}.csv.gz` in the [directory](../02_step_feature_to_final_dataframes/2022_XACT_seq_data).
    - global logos for each samples: `global_logo_{sample_names}.csv.gz` in the [directory](../02_step_feature_to_final_dataframes/2022_XACT_seq_data).




## From Feature files to grouped files

Feature files are the outputs of the first step of the pipeline which explained in the detailed in the [README](../01_step_fastq_to_feature/README.md) file.

The feature files from the first steps need to be deposited in the `pipeline_data` [directory](../02_step_feature_to_final_dataframes/pipeline_data).

Content of the `pipeline_data` folder:

``` bash
├── features_combined_CP49.txt
├── features_combined_CP50.txt
├── features_combined_CP51.txt
├── features_combined_CP52.txt
├── features_combined_CP53.txt
├── features_combined_CP54.txt
└── features_combined_template.txt
```

The `{sample_names}` feature files have the following format (e.g for `CP49`)

```
sample          bc              umi             var                                                     var_length
CP49_xactseq    GGCCGAGGTCGTTAG ATTACCGTAC      GGTTAAATGACACGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG     51
CP49_xactseq    CTTAACTTGCAGTTA TGGAACAACC      GGGTTAAATGTCATGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG    52
CP49_xactseq    CTTCGTCATCATAAT ACAGACAATA      GGTTAAGTTTATCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG     51
CP49_xactseq    CTAGTATGAGTCCGC AGCACAAATT      AATCAGATTGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG         47
CP49_xactseq    GGTGCATCGTTGTGT CTTCAATGGC      GGTTAAAAGTCTCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG     51
CP49_xactseq    GACAGATAGGCCCGG CACTCTAATA      GGGTTAATTATATCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG    52
CP49_xactseq    TTCCGGATCTGGATG AACTCACTAT      GGGTTAACCGGGTCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG    52
CP49_xactseq    AGTGGTCGAACCGGT ACGATAATGC      TTAATCGTGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG       49
CP49_xactseq    CTGGAGCAGCCTGGT CGACCTTTCA      TTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG                   37
```

The `template` feature file has the following format:

```
sample          bc              pe     
CP62T_xactseq   TTTGATCTGGGTTGG GACCCAG 
CP62T_xactseq   CAGAGTAGTTGTGAA GATGAAG 
CP62T_xactseq   AGGTGAGCCCTATGG TTGTCCG 
CP62T_xactseq   ATGGCTGGGATCATA GCTGCTT 
CP62T_xactseq   GCGTTGTATTAAACC TACGACT 
CP62T_xactseq   CCCTCGATTGCGGGC AATAATT 
CP62T_xactseq   TACAATGCCTGGTTT TTTCTTG 
CP62T_xactseq   TGGTAGTTCGAAGGA TATTCGC 
CP62T_xactseq   CAGGTGGGTAGCGGG GCATCGT 
```

In the above (and following) we used the following abbreviations:
- `bc`: barcode
- `pe`: pause element
- `umi`: unique molecular identifier
- `var`: variable length sequence
- `var_length`: length of the variable sequence.

1. First we make the `group` file from the template.

    - Template feature file has `name bc pe` columns.
    - We need to group `(bc, pe)` columns.
    - Get rid of those `(bc, pe)` samples with few counts: `min_ct`
    - to perform the above steps one can run the scrip as follow:
        - `python group_filter_template.py -t template -m min_ct`
        - `-t` arg: user-specified name of the template file. Default is `template`.
        - `-m` arg: user-specified minimum counts to be considered. Default is `5`.
    - the output of this script is a file:
        - `./grouped_filter_data/group_template.csv.gz`
    - there would be some information ans statistics about this step saved in the report file:
        - `./reports/template_group_filter_report.txt`


2. Second, we make the `group` file for each sample.

    - Samples feature files have `name  bc  umi var var_length` columns. 
    - We need to group `(bc, umi)` based on the mode of (most frequent occurrence of) the `var_length`. This step is the most time-consuming step and we used the `agg(mode)` from the `pandas` framework.
    - to perform the above steps one can run the scrip as follow:
        - `python group_filter_samples.py  -s {sample_names}`. 
    - output files of this scripts will be saved in: 
        - `./grouped_filter_data/` [directory](../02_step_feature_to_final_dataframes/grouped_filter_data) as
            ```bash
            ├── group_CP49.csv.gz
            ├── group_CP50.csv.gz
            ├── group_CP51.csv.gz
            ├── group_CP52.csv.gz
            ├── group_CP53.csv.gz
            ├── group_CP54.csv.gz
            ```
    -  statistics and reports are deposited in: 
        - `./reports` directory.
            ```bash
            ├── CP49_group_filter_report.txt
            ├── CP50_group_filter_report.txt
            ├── CP51_group_filter_report.txt
            ├── CP52_group_filter_report.txt
            ├── CP53_group_filter_report.txt
            ├── CP54_group_filter_report.txt
            ```

## From group files to merge files

The `group_{sample_names}.csv.gz` files for have the following format (e.g. for `CP49`):

```
umi,       bc,             var,                                                  var_length
AAAAAAAAAA,AATCAACAGGGGAAT,GGGTTAACATTAATGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG, 52
AAAAAAAAAA,ATTAACCTAAACCGT,GGGTTAATCTAATAGTTGTGGTAGTAAGATGAAAAGAGGCGGCGCCTGCAGG, 52
AAAAAAAAAA,GGAATTGAATTTCGT,GGGTTAAAAGAACAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG, 52
AAAAAAAAAC,ATATTTGGGAACCTG,GGTTAATCTATTAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,  51
AAAAAAAAAC,CGATGACCAGTCATT,GTTAAACACTAAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,   50
AAAAAAAAAG,CAGTAATAAGAATCG,GGATTAATTTATTCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG, 52
AAAAAAAAAG,GATCAACTTGCCGGT,GGATTAATTAGATCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG, 52
AAAAAAAAAG,TCCATGGTATATCTG,TTAATCGTTTAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,    49
AAAAAAAAAT,GCTGGCCCGTGAGTA,TGCTTAATATAAAATTTGTGTTATTGATATGAAAAGATTAGGCGCCTGCAGT, 52
```

The `group_template.csv.gz`, has the following format:

```
pe,     bc,              count_template
AAAAAAA,AAACCGCAGATGGCC, 31
AAAAAAA,ACAGGATGAGTGTGG, 9
AAAAAAA,CAGTCATGGTTGCTC, 73
AAAAAAA,CATTCCTTAGCCCTT, 29
AAAAAAA,CGAATGAATCGGGAG, 22
AAAAAAA,CGCTGTGTGACAACA, 8
AAAAAAA,CGGGTAGCGATGTGC, 43
AAAAAAA,GAGGCAAACAGTGCT, 27
AAAAAAA,GATAGACATCACGGT, 24
```

For each sample `(umi, bc)` pairs needed to be merge with the template `(pe, bc)` pairs on `bc` column.
- to perform this step one can run the script as follows:
    
    - `python make_merge_files.py  -s {sample_names} -t {template_name}`
    - `-s` arg: user-specified sample names.
    - `-t` arg: user-specified name of the template file. Default is `template`.

- outputs of this scrips deposited in the: 
    - `merged_samp_temp_data` [directory](../02_step_feature_to_final_dataframes/merged_samp_temp_data) as
        ```bash
        ├── CP49_template_merged.csv.gz
        ├── CP50_template_merged.csv.gz
        ├── CP51_template_merged.csv.gz
        ├── CP52_template_merged.csv.gz
        ├── CP53_template_merged.csv.gz
        └── CP54_template_merged.csv.gz
        ```

- statistics of the above merging step for each samples are reported in: 
    - `/reports` directory.
        ```bash
        ├── CP49_merge_report.txt
        ├── CP50_merge_report.txt
        ├── CP51_merge_report.txt
        ├── CP52_merge_report.txt
        ├── CP53_merge_report.txt
        ├── CP54_merge_report.txt
        ```

## From merged files to (pause element, A_location) count files

The `{sample_names}_template_merged.csv.gz` files produced in the previous step
have the following format:

```
umi,        bc,              var,                                                    var_length, pe,      count_template
AAAAAAAACC, ACCATGGGAGAGGTG, GGGTTAAACTTCGAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,   52,         ACTTCGA, 30
ACTCACAAAA, ACCATGGGAGAGGTG, GGGTTAAACTTCGAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,   52,         ACTTCGA, 30
AAAAAAAACC, GAAATGGTGCGGTTA, TAGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,            43,         TTTAGCC, 32
AAACAAAACC, GAAATGGTGCGGTTA, TAGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,            43,         TTTAGCC, 32
AAGATTGGTC, GAAATGGTGCGGTTA, GGGTTAATTTAGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,   52,         TTTAGCC, 32
ACCCGGGAAC, GAAATGGTGCGGTTA, AATTTAGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,        47,         TTTAGCC, 32
```

Here we need to count the frequence of `(pe, var_length)` pairs occurance for each sample.

- First we changed the `var_length` to `a_loc` (A-site location) to avoid confusion in presenting logos and be consistent with the manuscript. The **A-site** location, `a_loc`, can be find by `a_loc = 54-var_length`.

- to count the `(pe, a_loc)` for each sample one can run the following script:
    - `python count_pe_aloc_pairs.py -s {sample_names}`
    - `-s` arg: user-specified sample names.
- The output of the above script is deposited in : 
    - `pe_aloc_pairs_data` [directory](../02_step_feature_to_final_dataframes/pe_aloc_pairs_data). 
    - **The content of this directory is tracked by git and is avialable in the repository**
        ```bash
        ├── CP49_pe_aloc.csv.gz
        ├── CP50_pe_aloc.csv.gz
        ├── CP51_pe_aloc.csv.gz
        ├── CP52_pe_aloc.csv.gz
        ├── CP53_pe_aloc.csv.gz
        └── CP54_pe_aloc.csv.gz
        ```
    - The above files have the following formats (e.g. for `CP49_pe_aloc.csv.gz`)
        ```
        pe,       a_loc, count
        AAAAAAA,  0,     1
        AAAAAAA,  1,     4
        AAAAAAA,  2,     25
        AAAAAAA,  3,     10
        AAAAAAA,  4,     1
        AAAAAAA,  5,     1
        AAAAAAA,  6,     2
        AAAAAAA,  9,     1
        AAAAAAA,  1,     1
        ```

- some run-time statistics of this step are reported in the: 
    - `reports` directory.
        ```bash
        ├── CP49_pe_aloc_count_report.txt
        ├── CP50_pe_aloc_count_report.txt
        ├── CP52_pe_aloc_count_report.txt
        ├── CP53_pe_aloc_count_report.txt
        ├── CP54_pe_aloc_count_report.txt
        ```

## Weights for correcting the template bias

In this step we need to find the necessary corrections that needed to be apply for correcting the template biases as descriped in the manuscript. 

- The input of this step is `features_combined_template.csv.gz`. 
- We formed the enrichment logo for all the pause elements in the template.
- We used the [logomaker](https://logomaker.readthedocs.io/en/latest/) Python package to find the probability logos for the pause elements and the final dataframe is saved to be used for template correction in each position.
- To do so, one can run the following script:
    - `python make_template_weight.py`
- The output of this script is a file:
    - [2022_XACT_seq_data/template_weight_sigma_df.csv.gz](../02_step_feature_to_final_dataframes/2022_XACT_seq_data/template_weight_sigma_df.csv.gz) which is saved in this repository.

## Ligation and Cross-link corrections from XACT-seq (2020)

The similar computational pipeline has been used to analyse the XACT-seq (2020) experiments. The raw fastq files can be downloaded from the from SRA BioProject number [SRP254182](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP254182).

1. First, we performed the first step discribed in this repo to analyse the samples from XACT-seq (2020) experiments and get the featrue files for each sample and the template.
2. Second, we rescaled the counts for all the samples from XACT-seq (2020) with template of XACT-seq (2020) called `CP26T`.
3. The enrichement logos for cross-linking at positions +6, +7 and +8 are then averaged over all the +Rif replicates to get the averaged cross-link and ligation biases which have been used to rescale the counts of the current experiments.
4. The +Rif replicates are `CP22, CP24, CP28`.
5. The finial averaged cross-link and ligation bias correction weigths are given in [xlink_lig_ave_xact_seq.csv.gz](02_step_feature_to_final_dataframes/xact_seq_bias_data/xlink_lig_ave_xact_seq.csv.gz)
6. The detailed of this step is described in the method section of the manuscript.

## Rescale the counts
In this step we will make the **final dataframes** ready for plotting the logos and count profiles in the manuscript. 
Here we:
- Correct each sample with the template.
- Correct each sample with ligation and cross-link bias from XACT-seq (2020)
- To perform the above steps run the following script:
    - `python make_rescaled_counts.py`
- output files of the script is deposited in the `2022_XACT_seq_data` [directory](../02_step_feature_to_final_dataframes/2022_XACT_seq_data) with following pattern:

    - The rescaled counts for each sample: `{sample_names}_rescaled.csv.gz`
    - The global logo for each sample: `global_log_{sample_names}.csv.gz`
    - The rescaled counts values for each sample: `rescaled_counts_{sample_names}.csv.gz`
    - **These files (all the contents of the `2022_XACT_seq_data`) will be tracked by git and will be used to make a final logos.**