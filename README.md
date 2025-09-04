# RNA Read Alignment and Counting using Snakemake
This simple Snakemake workflow uses `FastQC` to QC the paired read fastq files, `HISAT` to align the reads and `featureCounts` to quantify how many reads map to each gene in GRCh38. I run the Snakemake file using `RunSnakemake.sh` on a HPC! The whole workflow took ~2.5 hours for 7 samples. Here I have listed each step: variables in curly braces are specified by snakemake rules (see `Snakefile.py`).

![](https://github.com/alicesmail12/Snakemake-RNA-Sequencing/blob/main/RNA-seq-DAG.png?raw=true)

### Steps
**Step 1: FastQC**

First I used `FastQC`, which analyses FASTQ files and creates a **HTML quality check report**, including quality scores for each read and base position, as well as assessments of GC content, nucleotide distribution, read length, overrepresented sequences and adapter content. 

In a snakemake workflow on a HPC this is how FastQC can be run:
```bash
# Modules
module load FastQC

# Run
fastqc {File}_R{Read}.fastq -o {FASTQC_DIR}
```

![](https://github.com/alicesmail12/Snakemake-WGS/blob/main/FASTQC.png?raw=true)
<p align="center"><i>Example FastQC Output</i></p>

**Step 2: HISAT Alignment**

Next I used `HISAT2` to align the RNAseq reads to a reference genome. `SAMtools sort` then sorts the resulting BAM files by coordinate.

```bash
# Modules
module load HISAT2 gompi SAMtools

# Run
hisat2 -x {params.index} -1 {input.R1} -2 {input.R2} -p 12 --dta --rna-strandness RF --summary-file {output.sum} --time | samtools sort -o {output.bam}
```

**Step 3: featureCounts**

Then I can use `featureCounts` from Subread to count the number of RNAseq reads mapped to each regions of the reference genome.

```bash
# Modules
module load Subread

# Run
featureCounts -p --countReadPairs -a {params.genefile} -o {output.counts} {input.bam}
```

**Step 4: Gather counts**

Last I can print all the count columns to a new file.

```bash
# Run
cat {input.counts} | cut -f1,7 > {output.countsOnly}
```
