# RNA Read Alignment and Counting using Snakemake
This simple Snakemake workflow (`Snakefile`) uses `FastQC` to QC the paired read fastq files, `HISAT` to align the reads and `FeatureCounts` to quantify how many reads map to each gene in GRCh38. I run the Snakemake file using `RunSnakemake.sh` on a HPC! The whole workflow takes ~2.5 hours for 7 samples.

