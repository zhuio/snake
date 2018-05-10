# 程序出入口
import os
pwd = os.path.abspath('.')

rule all:
    input:
        expand('{sample}.assemblies.fasta.transdecoder.genome.gff3', sample=['sample.sqlite'])

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
        r = rules.cat.output
    output:
        'transcripts.fasta.clean'
    shell:
        """
        $PASAHOME/bin/seqclean {input.r} -v vectors.fasta
        """


rule accession_extractor:
    input:
        r = 'Trinity.fasta'
    output:
        'tdn.accs'
    shell:
        """
        $PASAHOME/misc_utilities/accession_extractor.pl < {input.r} > {output}
        """


rule Launch_PASA_pipeline:
    input:
        r = 'alignAssembly.config',
        r1 = rules.seqclean.output,
        r2 = 'genome.fasta',
        r3 = rules.accession_extractor.output,
        pwd = pwd
    output:
        '{sample}.assemblies.fasta',
        '{sample}.pasa_assemblies.gff3'
    shell:
        """
        sudo docker pull pasapipeline/pasapipeline \
        && sudo docker run --rm -it \
      -v /tmp:/tmp \
      -v {input.pwd}:{input.pwd}  \
       pasapipeline/pasapipeline:latest \
        bash -c 'cd {input.pwd} \
              && /usr/local/src/PASApipeline/Launch_PASA_pipeline.pl \
              -c {input.r} -C -R \
              --ALIGNER gmap -g {input.r2} -t {input.r1} \
              --TDN {input.r3}'
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
        sudo docker run --rm -it \
      -v /tmp:/tmp \
      -v {input.pwd}:{input.pwd}  \
       pasapipeline/pasapipeline:latest \
       bash -c 'cd {input.pwd} \
             && /usr/local/src/PASApipeline/scripts/pasa_asmbls_to_training_set.dbi \
       --pasa_transcripts_fasta {input.r} \
       --pasa_transcripts_gff3 {input.r1}
        """
