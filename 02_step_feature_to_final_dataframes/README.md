# Features to final dataframes

This folder contains scripts, which run on the `Elzar` High Performance Computing Cluster at Cold Spring Harbor Laboratory (CSHL).
Scripts provided here are for the **second step** in our overall pipeline to get the sequence logos provided in the paper: 

**Structural and mechanistic basis of σ-dependent transcriptional pausing**

Scripts for first and third (final) steps are provided in the root directory.

Note that, due to the size of intermediate files, we are not providing them here.However, the structure of the directory (including empty folders) are given for clarity.

For ligation and crosslink biases correction we used the data from the following manuscript which we will refer in the following documentation as XACT-seq (2020):

**Winkelman, Jared T., et al. "XACT-seq comprehensively defines the promoter-position and promoter-sequence determinants for initial-transcription pausing." Molecular cell 79.5 (2020): 797-811.**

## TL;DR

The final outcome of this step which are provided in the git repository are:

1. `./2022_XACT_seq_data` folder:
    - template correction weights.
    - samples corrected by (a) the template from 2022 experiment and (b) by ligation and crosslink biases from XACT-seq (2020) experiment.
    - rescaled counts for each sample.
    - The content of this folder is used to plot the final logos in the **third step** of the pipeline.

2. raw pause-element, A-site location dataframes in `./pe_aloc_pairs_data`.

- `python group_filter_template.py -t template -m min_ct`
- `python group_filter_samples.py  -s {sample_names}`. For `sample_names` in `{CP49, CP50, CP51, CP52, CP53, CP54}`
- `python make_merge_files.py  -s {sample_name} -t {tamplate_name}`
- `python count_pe_aloc_pairs.py -s {sample_names}`

(note the following steps need `logomaker` Python package.)
- `python make_template_weight.py`
- `python make_rescaled_counts.py`


## fastq files to feature files

`fastq` files for samples and templates are processed with in-house pipeline
which is also provided in the root directory (first step: `fastq_to_features`).
Outputs of the first step are **feature files**.

## From Feature files to grouped files
Feature files are provided to this pipeline in `pipeline_data` folder.

Content of the `./pipeline_data` folder:

``` bash
├── features_combined_CP49.txt
├── features_combined_CP50.txt
├── features_combined_CP51.txt
├── features_combined_CP52.txt
├── features_combined_CP53.txt
├── features_combined_CP54.txt
└── features_combined_template.txt
```

The sample feature files `CP49, CP50, CP51, CP52, CP53` and `CP54` have the following format
```
sample          bc              umi             var                                                     var_length
CP49_xactseq    GGCCGAGGTCGTTAG ATTACCGTAC      GGTTAAATGACACGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG     51
CP49_xactseq    CTTAACTTGCAGTTA TGGAACAACC      GGGTTAAATGTCATGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG    52
CP49_xactseq    CTTCGTCATCATAAT ACAGACAATA      GGTTAAGTTTATCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG     51
CP49_xactseq    CTAGTATGAGTCCGC AGCACAAATT      AATCAGATTGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG 47
CP49_xactseq    GGTGCATCGTTGTGT CTTCAATGGC      GGTTAAAAGTCTCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG     51
CP49_xactseq    GACAGATAGGCCCGG CACTCTAATA      GGGTTAATTATATCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG    52
CP49_xactseq    TTCCGGATCTGGATG AACTCACTAT      GGGTTAACCGGGTCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG    52
CP49_xactseq    AGTGGTCGAACCGGT ACGATAATGC      TTAATCGTGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG       49
CP49_xactseq    CTGGAGCAGCCTGGT CGACCTTTCA      TTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG   37
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


In the above (and following):
- `bc`: barcode
- `pe`: pause element
- `umi`: unique molecular identifier
- `var`: variable length sequence
- `var_length`: length of the variable sequence.

#### Template file to grouped file

Template feature file has `name bc pe` columns.

1. We need to group `(bc, pe)` columns.

2. Get rid of those `(bc, pe)` samples with few counts: `min_ct`
    
- running the script:

    - `python group_filter_template.py -t template -m min_ct`
    - `-t` arg: user-specified name of the template file. Default is `template`.
    - `-m` arg: user-specified minimum counts to be considered. Default is `5`.

- output file:

    - `./grouped_filter_data/group_template.csv.gz`

- report file:

    - `./reports/template_group_filter_report.txt`

#### Sample files to group files

Samples feature files have `name  bc  umi var var_length` columns. 

1. We need to group `(bc, umi)` based on the mode of (most frequent occurrence of) the `var_length`. 
This step is the most time-consuming step and we used the `agg(mode)` from the `pandas` framework.

- running scripts:
    - `python group_filter_samples.py  -s {sample_names}`. For `sample_names` in `{CP49, CP50, CP51, CP52, CP53, CP54}`
- output files: 
    - `./grouped_filter_data/` directory.
- report files: 
    - `./reports` directory.

Content of `./grouped_filter_data/` directory:

```bash
├── group_CP49.csv.gz
├── group_CP50.csv.gz
├── group_CP51.csv.gz
├── group_CP52.csv.gz
├── group_CP53.csv.gz
├── group_CP54.csv.gz
```

with following reports in `./reports/` directory:

```bash
├── CP49_group_filter_report.txt
├── CP50_group_filter_report.txt
├── CP51_group_filter_report.txt
├── CP52_group_filter_report.txt
├── CP53_group_filter_report.txt
├── CP54_group_filter_report.txt
```

## From grouped files to merged files

The `group_{sample_names}.csv.gz` files for `sample_names={CP49 to CP54}`, produced in the previous step
have the following format:

```
umi,       bc,             var,                                                 var_length
AAAAAAAAAA,AATCAACAGGGGAAT,GGGTTAACATTAATGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,52
AAAAAAAAAA,ATTAACCTAAACCGT,GGGTTAATCTAATAGTTGTGGTAGTAAGATGAAAAGAGGCGGCGCCTGCAGG,52
AAAAAAAAAA,GGAATTGAATTTCGT,GGGTTAAAAGAACAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,52
AAAAAAAAAC,ATATTTGGGAACCTG,GGTTAATCTATTAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,51
AAAAAAAAAC,CGATGACCAGTCATT,GTTAAACACTAAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,50
AAAAAAAAAG,CAGTAATAAGAATCG,GGATTAATTTATTCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,52
AAAAAAAAAG,GATCAACTTGCCGGT,GGATTAATTAGATCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,52
AAAAAAAAAG,TCCATGGTATATCTG,TTAATCGTTTAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,49
AAAAAAAAAT,GCTGGCCCGTGAGTA,TGCTTAATATAAAATTTGTGTTATTGATATGAAAAGATTAGGCGCCTGCAGT,52
```

The grouped template file, `group_template.csv.gz`, have the following format:

```
pe,     bc,             count_template
AAAAAAA,AAACCGCAGATGGCC,31
AAAAAAA,ACAGGATGAGTGTGG,9
AAAAAAA,CAGTCATGGTTGCTC,73
AAAAAAA,CATTCCTTAGCCCTT,29
AAAAAAA,CGAATGAATCGGGAG,22
AAAAAAA,CGCTGTGTGACAACA,8
AAAAAAA,CGGGTAGCGATGTGC,43
AAAAAAA,GAGGCAAACAGTGCT,27
AAAAAAA,GATAGACATCACGGT,24
```

For each grouped sample `(umi, bc)` pairs needed to be merge with the grouped template `(pe, bc)` pairs on `bc` column. Outputs of this step are `sample_name_template_merged` csv files.


- running the script:
    
    - `python make_merge_files.py  -s {sample_name} -t {tamplate_name}`
    - `-s` arg: user-specified sample names.
    - `-t` arg: user-specified name of the template file. Default is `template`.

- output files: 
    - `./merged_samp_temp_data` directory.

```bash
├── CP49_template_merged.csv.gz
├── CP50_template_merged.csv.gz
├── CP52_template_merged.csv.gz
├── CP53_template_merged.csv.gz
└── CP54_template_merged.csv.gz
```

- report files: 
    - `./reports` directory.

```bash
├── CP49_merge_report.txt
├── CP50_merge_report.txt
├── CP52_merge_report.txt
├── CP53_merge_report.txt
├── CP54_merge_report.txt
```

### From merged files to count (pe, A_location) files

The `{sample_names}_merged.csv.gz` files for `sample_names={CP49 to CP54}`, produced in the previous step
have the following format:

```
umi,bc,var,var_length,pe,count_template
AAAAAAAACC,ACCATGGGAGAGGTG,GGGTTAAACTTCGAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,52,ACTTCGA,30
ACTCACAAAA,ACCATGGGAGAGGTG,GGGTTAAACTTCGAGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,52,ACTTCGA,30
AAAAAAAACC,GAAATGGTGCGGTTA,TAGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,43,TTTAGCC,32
AAACAAAACC,GAAATGGTGCGGTTA,TAGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,43,TTTAGCC,32
AAGATTGGTC,GAAATGGTGCGGTTA,GGGTTAATTTAGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,52,TTTAGCC,32
ACCCGGGAAC,GAAATGGTGCGGTTA,AATTTAGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,47,TTTAGCC,32
ACTAGGAATC,GAAATGGTGCGGTTA,TAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,31,TTTAGCC,32
ACTATGAATC,GAAATGGTGCGGTTA,TAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,31,TTTAGCC,32
ATGATTGCTT,GAAATGGTGCGGTTA,TAATTTAGCCGTTGTGGTAGTGAGATGAAAAGAGGCGGCGCCTGCAGG,48,TTTAGCC,32
```

For each of `{sample_names}_merged` files we need to count `(pe, var_length)` pairs.

In this step we also change the `var_length` to `a_loc` (A-site location) for avoid confusion in presenting logos and be consistent with the manuscript. 
The **A-site** location `a_loc` can be find by

`a_loc = 54-var_length`

- running the script:
    - `python count_pe_aloc_pairs.py -s {sample_names}`
    - `-s` arg: user-specified sample names.
    

- output files: 
    - `./pe_aloc_pairs_data` directory. 
    - **These are the first outputs of the second step of our pipeline and they will be saved for further postprocessing and will be tracked with git.**

```bash
├── CP49_pe_aloc.csv.gz
├── CP50_pe_aloc.csv.gz
├── CP51_pe_aloc.csv.gz
├── CP52_pe_aloc.csv.gz
├── CP53_pe_aloc.csv.gz
└── CP54_pe_aloc.csv.gz
```

- report files: 
    - `./reports` directory.

```bash
├── CP49_pe_aloc_count_report.txt
├── CP50_pe_aloc_count_report.txt
├── CP52_pe_aloc_count_report.txt
├── CP53_pe_aloc_count_report.txt
├── CP54_pe_aloc_count_report.txt
```

## (pe, a_loc, count) dataframes 

The `{sample_names}_pe_aloc.csv.gz` are tracked with git and have the following pattern.

```
pe,       a_loc, count
AAAAAAA,  0     ,1
AAAAAAA,  1     ,4
AAAAAAA,  2     ,25
AAAAAAA,  3     ,10
AAAAAAA,  4     ,1
AAAAAAA,  5     ,1
AAAAAAA,  6     ,2
AAAAAAA,  9     ,1
AAAAAAA,  11    ,1
```

## Template weights (for template correction step)

In this step we used the [logomaker](https://logomaker.readthedocs.io/en/latest/) Python package to find the probability logos for the pause elements in the `features_combined_template`. By forming the enrichement values for those pause element we saved the correpsonding weigths for each nucleotide in each position. This file will be used for template correction described in the manuscript.


- running the script:
    - `python make_template_weight.py`

- output file:

    - `./2022_XACT_seq_data/template_weight_sigma_df.csv.gz`
    - **This file (all the contents of the `2022_XACT_seq_data`) will be tracked by git and will be used to make a final logos.**


## Ligation and Cross-link correction from XACT-seq (2020)

The similar computational pipeline has been used to make the average cross-link and ligation biases from the XACT-seq (2020) experiments. The detailed mathematical procedure of the steps are provided in the manuscript. The final dataframe for the above correction is given in the follwing dataframe:

- `./xact_seq_bias_data/xlink_lig_ave_xact_seq.csv.gz` which contains the weight for each nucleotide `A,C,G,T` for each position in pause elements, needed to be corrected.

In this step we will make the **final dataframes** for plotting the logos provided in the manuscript. These dataframes are corrected by
- The current experiment template
- The ligation and cross-link biases from XACT-seq (2020)
The final rescaled counts (after all corrections) as well as global logos (averaged over all the replicates) are also given.

- running the script:
    - `python make_rescaled_counts.py`

- output files:

    - `./2022_XACT_seq_data/{sample_names}_rescaled.csv.gz`
    - `./2022_XACT_seq_data/global_log_{sample_names}.csv.gz`
    - `./2022_XACT_seq_data/rescaled_counts_{sample_names}.csv.gz`
    - **These files (all the contents of the `2022_XACT_seq_data`) will be tracked by git and will be used to make a final logos.**