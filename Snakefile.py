# Filename wildcards
FILES = ['File1', 'File2']
READS = [1, 2]

# Directories and files
FASTQ_DIR = './Experiment_Fastq/'
FASTQC_DIR = './FastQC-Output/'
HISAT_DIR = './HISAT2/'
COUNTS_DIR = './FeatureCounts/'

# Rule all
rule all:
    input:
        expand(os.path.join(FASTQC_DIR, '{File}_R{Read}_001_fastqc.html'), File=FILES, Read=READS),
        expand(os.path.join(COUNTS_DIR, '{File}_Counts.txt'), File=FILES)
        
# Step 1: FastQC
rule Get_FastQC:
  input:
    os.path.join(FASTQ_DIR, '{File}_R{Read}_001.fastq.gz')
  output:
    os.path.join(FASTQC_DIR, '{File}_R{Read}_001_fastqc.{Filetype}')
  shell:
    """
    #!/bin/bash
    fastqc {input} -o {FASTQC_DIR}
    """
    
# Step 2: trim reads (not required here as no adapter sequences detected using FastQC)
 
# Step 3: HISAT alignment
rule HISAT_Align:
  input:
    R1 = os.path.join(FASTQ_DIR, '{File}_R1_001.fastq.gz'),
    R2 = os.path.join(FASTQ_DIR, '{File}_R2_001.fastq.gz')
  params:
    index = './HISAT2/grch38/genome'
  output:
    bam = os.path.join(HISAT_DIR, '{File}.bam'),
    sum = os.path.join(HISAT_DIR, '{File}.summary.txt')
  shell:
    """
    #!/bin/bash
    hisat2 -x {params.index} -1 {input.R1} -2 {input.R2} -p 12 --dta --rna-strandness RF --summary-file {output.sum} --time | samtools sort -o {output.bam}
    """
    
# Step 4: FeatureCounts
rule Get_Counts:
  input:
    bam = os.path.join(HISAT_DIR, '{File}.bam')
  params:
    genefile = "./FeatureCounts/Homo_sapiens.GRCh38.113.gtf.gz"
  output:
    counts = os.path.join(COUNTS_DIR, '{File}_featureCounts.txt')
  shell:
    """
    #!/bin/bash
    featureCounts -p --countReadPairs -a {params.genefile} -o {output.counts} {input.bam}
    """

# Step 5: Counts only
rule Get_CountsOnly:
  input:
    counts = os.path.join(COUNTS_DIR, '{File}_featureCounts.txt')
  output:
    countsOnly = os.path.join(COUNTS_DIR, '{File}_Counts.txt')
  shell:
    """
    #!/bin/bash
    cat {input.counts} | cut -f1,7 > {output.countsOnly}
    """
