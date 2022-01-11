1. Step 1: `01_step_fastq_to_feature`: 

    - This component run on  

    - Scripts provides in this directory was configured specifically for the `Elzar` cluster at CSHL, and will likely have to be modified before it is run on a different cluster. 
    - To run this pipeline, first we need all `fastq` sequencing data and deposit them into the directory `/01_step_fastq_to_feature/fastq` directory. **WHERE DOES ONE GET THESE?**
    - The name of the `fastq` files should be matched with the `01_step_fastq_to_feature/var_seq/090821_xactseq.xlsx` metadate file. **RENAME METADATA FILE TO BE LESS CRYPTIC**
    - To run the pipeline one can execute `python run_pipeline.py var_seq`. **WHAT DOES VAR_SEQ STAND FOR? WHY IS IT NEEDED AS AN ARGUMENT?**
    - The output of this step is called `feature` files which are explained in details in the `Step 2`. 