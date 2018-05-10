import os

pwd = os.path.abspath('.')
DATABASE = ['rrrrr.sqlite']

rule all:
    input:
        expand('{sample}.assemblies.fasta.transdecoder.genome.gff3', sample=DATABASE),
        'error.out'

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
	sudo docker pull pasapipeline/pasapipeline \
        && sudo docker run --rm -it \
        -v {input.pwd}:{input.pwd} \
        pasapipeline/pasapipeline:latest \
        bash -c 'cd {input.pwd} \
        && /usr/local/src/PASApipeline/bin/seqclean {input.r} -v vectors.fasta'
        """

rule accession_extractor:
    input:
        r = 'Trinity.fasta',
        pwd = pwd
    output:
        'tdn.accs'
    shell:
        """
        sudo docker run --rm -it \
        -v {input.pwd}:{input.pwd} \
        pasapipeline/pasapipeline:latest \
        bash -c 'cd {input.pwd} \
              && /usr/local/src/PASApipeline/misc_utilities/accession_extractor.pl < {input.r} > {output}'
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
        sudo docker run --rm -it \
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

rule simplifyFastaHeaders:
    input:
        r = 'Trinity.fasta',
        r1 = 'genome.fasta'
    output:
        'cdna.fa',
        'genome.fasta.clean'
    shell:
        """
        simplifyFastaHeaders.pl {input.r} nameStem {output[0]} header.map
        simplifyFastaHeaders.pl {input.r1} nameStem {output[1]} header.map
        """

rule autoAug:
    input:
        r = "genome.fasta",
        r1 = "Trinity.fasta",
        r2 = "genome.gff3"
    output:
        'error.out'
    shell:
        "autoAug.pl --species="+ species_name + " --genome={input.r} --cdna={input.r1} --trainingset={input.r2} --useexisting \
        1>> debug.out 2>> error.out && \ "
        """
        cd autoAug/autoAugPred_abinitio/shells && \
        sed -i 's/qsub -cwd/bash/g' * && \
        ./shellForAug && \
        cd ../../../ && \
        """
        "autoAug.pl --species="+ species_name + " --genome={input.r} --cdna={input.r1} --trainingset={input.r2} --useexisting \
        1>> debug.out 2>> error.out && \ "
        """
        cd autoAug/autoAugPred_hints/shells && \
        sed -i 's/qsub -cwd/bash/g' * && \
        ./shellForAug && \
        cd ../../../ && \
        """
        "autoAug.pl --species="+ species_name + " --genome={input.r} --cdna={input.r1} --trainingset={input.r2} --useexisting \
        1>> debug.out 2>> error.out && \ "
