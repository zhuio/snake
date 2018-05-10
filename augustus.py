# augustus脚本 需要修改26行物种名字

rule all:
    input:
        'autoAug/autoAugPred_abinitio/predictions/augustus.aa'

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
        r = 'genome.fasta.clean',
        r1 = 'cdna.fa',
        r2 = "genome.gff3"
    output:
        'autoAug/autoAugPred_abinitio/predictions/augustus.aa'
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
