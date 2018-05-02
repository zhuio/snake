# 程序出入口

rule all:
    input:
        'trinity_out_dir/Trinity.fasta',
        'trinity_genomeguide_dir/Trinity-GG.fasta'


# # genome组装
# rule spades:
#     input:
#         r1 = 'genome/1261_poplar_genome.1.fq',
#         r2 = 'genome/1261_poplar_genome.2.fq'
#     output:
#         'output_dir/scaffolds.fasta'
#     shell:
#         "spades.py -o output_dir --careful -m 30 -1 {input.r1} -2 {input.r2}"

# hisat2比对生成bam文件
rule hisat2:
    input:
        r = 'genome/genome.fasta',
        r1 = 'rnaseq/1306_australis_rnaseq.1.fq',
        r2 = 'rnaseq/1306_australis_rnaseq.2.fq'
    output:
        '1306_australis_rnaseq.sam'
    shell:
        """
        hisat2-build {input.r} genome
        hisat2 -x genome -1 {input.r1} -2 {input.r2} -S {output}
        """

# samtools排序
rule samtools:
    input:
        rules.hisat2.output
    output:
        '1306_australis_rnaseq.bam'
    shell:
        "samtools sort {input} -o {output}"

# trinty组装
rule trinity:
    input:
        r = rules.samtools.output,
        r1 = 'rnaseq/1306_australis_rnaseq.1.fq',
        r2 = 'rnaseq/1306_australis_rnaseq.2.fq'
    output:
        'trinity_out_dir/Trinity.fasta',
        'trinity_genomeguide_dir/Trinity-GG.fasta'
    shell:
        """
        Trinity --seqType fq --max_memory 30G --left {input.r1} --right {input.r2} --CPU 12
        Trinity --genome_guided_bam {input.r} --max_memory 30G --genome_guided_max_intron 10000 --CPU 12 --output trinity_genomeguide_dir
        """
