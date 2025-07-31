#!/bin/bash
#SBATCH --output=Snakemake.out
#SBATCH -p {node}
#SBATCH --mem=64G
#SBATCH -c 12

# Create directories
cd /Alice/RNAseq-Pipeline-Snakemake/
if [ ! -d ./FastQC-Output/ ]; then mkdir -p ./FastQC-Output/; fi
if [ ! -d ./HISAT2/ ]; then mkdir -p ./HISAT2/; fi
if [ ! -d ./FeatureCounts/ ]; then mkdir -p ./FeatureCounts/; fi

# Load required modules
module load R Graphviz snakemake
module load FastQC HISAT2/2.1.0-foss-2017b gompi/2017b SAMtools/1.11-GCC-10.2.0 Subread/2.0.3-GCC-11.2.0

# Snakemake DAG
snakemake -c12 --dag ./FeatureCounts/Sample1_Counts.txt ./FastQC-Output/Sample1_fastqc.html | dot -Tsvg > dag.svg

# Run Snakefile using 12 cores
snakemake -c12
