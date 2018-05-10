# 需要snakemake，docker在root权限下运行，

import os

pwd = os.path.abspath('.')
DATABASE = ['test.sqlite']

rule all:
    input:
        expand('{sample}.assemblies.fasta.transdecoder.genome.gff3', sample=DATABASE),


rule cat:
    input:
        r = 'Trinity.fasta',
        r1 = 'Trinity-GG.fasta'
    output:
        'transcripts.fasta'
    shell:
        """
        cat {input.r} {input.r1} > {output}
        """

rule seqclean:
    input:
        r = rules.cat.output,
        pwd = pwd
    output:
        'transcripts.fasta.clean'
    shell:
        """
	docker pull pasapipeline/pasapipeline \
        && docker run --rm -it -e USER='zhu'\
        -v {input.pwd}:{input.pwd} \
        pasapipeline/pasapipeline:latest \
        bash -c 'cd {input.pwd} \
        && /usr/local/src/PASApipeline/bin/seqclean {input.r} -v vectors.fasta'
        """



rule Launch_PASA_pipeline:
    input:
        r = 'alignAssembly.config',
        r1 = rules.seqclean.output,
        r2 = 'genome.fasta',
        pwd = pwd
    output:
        '{sample}.assemblies.fasta',
        '{sample}.pasa_assemblies.gff3'
    shell:
        """
         docker run --rm -it \
      -v /tmp:/tmp \
      -v {input.pwd}:{input.pwd}  \
      -e USER='zhu' \
       pasapipeline/pasapipeline:latest \
        bash -c 'cd {input.pwd} \
              && /usr/local/src/PASApipeline/Launch_PASA_pipeline.pl \
              -c {input.r} -C -R \
              --ALIGNER gmap -g {input.r2} -t {input.r1} \
              -T -u transcripts.fasta'
        """

rule pasa_asmbls_to_training_set:
    input:
        r = rules.Launch_PASA_pipeline.output[0],
        r1 = rules.Launch_PASA_pipeline.output[1],
        pwd = pwd
    output:
        '{sample}.assemblies.fasta.transdecoder.genome.gff3'
    shell:
        """
         docker run --rm -it \
      -v /tmp:/tmp \
      -v {input.pwd}:{input.pwd}  \
      -e USER='zhu' \
       pasapipeline/pasapipeline:latest \
       bash -c 'cd {input.pwd} \
             && /usr/local/src/PASApipeline/scripts/pasa_asmbls_to_training_set.dbi \
       --pasa_transcripts_fasta {input.r} \
       --pasa_transcripts_gff3 {input.r1}'
        """
