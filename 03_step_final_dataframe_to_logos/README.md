# Making sequence logos and count profiles

Scripts provided here are for the **third (final) step** in our overall pipeline to get the sequence logos and recount profiles provided in the paper: 

**Structural and mechanistic basis of σ-dependent transcriptional pausing**

Scripts for the [first](../01_step_fastq_to_feature) and [second](../02_step_feature_to_final_dataframes) steps are provided in the root directory.
Scripts in this step depend on popular scientific python packages like `numpy, pandas` and `matplotlib`. In addition, for sequence logos we used the Python package [logomaker](https://logomaker.readthedocs.io/en/latest/).

To reproduce the figures presented in this manuscript, execute the following iPython notebooks:

1. [`2014_Vvedenskaya_figs.ipynb`](../03_step_final_dataframe_to_logos/2014_Vvedenskaya_sites/2014_Vvedenskaya_figs.ipynb):
    - Sequence logo for [Vvedenskaya, Irina O., et al. "Interactions between RNA polymerase and the “core recognition element” counteract pausing." Science 344.6189 (2014): 1285-1289](https://doi.org/10.1126/science.1253458) paper.
    - The corresponding data to produce the figure is in [Pause_sites_Vvedenskaya_2014.xlsx](../03_step_final_dataframe_to_logos/2014_Vvedenskaya_sites/Pause_sites_Vvedenskaya_2014.xlsx) 


2. [`2020_XACT_seq_logos_figs.ipynb`](../03_step_final_dataframe_to_logos/2020_XACT_seq/2020_XACT_seq_logos_figs.ipynb):
    - Sequence logos and rescaled count profiles the XACT_seq (2020) paper.
    [Winkelman, Jared T., et al. "XACT-seq comprehensively defines the promoter-position and promoter-sequence determinants for initial-transcription pausing." Molecular cell 79.5 (2020): 797-811](https://doi.org/10.1016/j.molcel.2020.07.006).
    - The corresponding data to produce the figures are in [2020_XACT_seq_data](../03_step_final_dataframe_to_logos/2020_XACT_seq/2020_XACT_seq_data). These data are produced by running our pipeline on the raw fastq files from the SRA BioProject number [SRP254182](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP254182) as explained in the [README](../02_step_feature_to_final_dataframes/README.md) file.
    - The final figures are deposited in [2020_XACT_seq_figs](../03_step_final_dataframe_to_logos/2020_XACT_seq/2020_XACT_seq_figs).

3. [`2022_XACT_seq_logos_figs.ipynb`](../03_step_final_dataframe_to_logos/2022_XACT_seq/2022_XACT_seq_logos_figs.ipynb):
    - Sequence logos and count profiles for the experiments conducted for the current manuscript.
    - The corresponding data to produce the figures are in [2022_XACT_seq_data](../03_step_final_dataframe_to_logos/2022_XACT_seq/2022_XACT_seq_data). These data are produced by running our pipeline on the raw fastq files from the SRA BioProject number [SRP355098](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP355098) as explained in the [README](../02_step_feature_to_final_dataframes/README.md) file.

    - The final figures are deposited in [2022_XACT_seq_figs](../03_step_final_dataframe_to_logos/2022_XACT_seq/2022_XACT_seq_figs).