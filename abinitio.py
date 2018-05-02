# 程序出入口

rule all:
    input:
        # expand('{sample}.fasta.transdecoder.pep', sample=['rose3.sqlite']),
        'final.fasta.transdecoder.pep'

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
        r4 = 'alignAssembly.config',
        r5 = rules.seqclean.output
    output:
        'final.fasta',
        'final.gff3'
    shell:
        """
        $PASAHOME/Launch_PASA_pipeline.pl \
        -c {input.r} -t {input.r1} -C -R -g \
        {input.r2} --ALIGNERS blat,gmap --CPU 2 \
        --TDN {input.r3}
        """
        """
        $PASAHOME/scripts/build_comprehensive_transcriptome.dbi \
        -c {input.r4} -t {input.r5} --min_per_ID 95 --min_per_aligned 30
        """
        """
        mv compreh_init_build/compreh_init_build.fasta final.fasta
        mv compreh_init_build/compreh_init_build.gff3 final.gff3
        """



rule pasa_asmbls_to_training_set:
    input:
        r = rules.Launch_PASA_pipeline.output[0],
        r1 = rules.Launch_PASA_pipeline.output[1],
    output:
        'final.fasta.transdecoder.pep'
    shell:
        """
        $PASAHOME/scripts/pasa_asmbls_to_training_set.dbi \
       --pasa_transcripts_fasta {input.r} \
       --pasa_transcripts_gff3 {input.r1}
        """
