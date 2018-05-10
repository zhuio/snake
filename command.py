SNAP version 2009-02-03 or higher (for eukaryotic genomes).
Augustus 2.0 or higher (for eukaryotic genomes)
GeneMark-ES (for eukaryotic genomes)
1. genome.fasta
    基因组序列文件。
2. inchworm.fasta
    转录组组装结果文件。此文件内容代表转录子序列或 EST 序列。为了增加其准确性，我个人选用了 trinity 中 inchworm 的结果文件，而不是转录组最终的组装结果文件。
3. proteins.fasta
    临近物种的蛋白质序列。可以从 NCBI 的 Taxonomy 数据库中下载。
4. consensi.fa.classified
    适合本物种的重复序列数据库。该文件是一个fasta文件，其序列代表着本物种的高重复序列。该文件使用 RepeatModeler 制作。
5. Augustus hmm files [species]
    适合本物种的 Augustus 的 HMM 文件。该文件以文件夹形式存放在 /opt/biosoft/augustus-3.0.3/config/species/ 目录下。将 genome.fasta 和 inchworm.fasta 输入 PASA，得到用于 trainning 的基因，然后使用 Augustus 进行 training，得到 HMM 文件。
6. Snap hmm file [species.hmm]
    适合本物种的 SNAP 的 HMM 文件。该文件是一个单独的文件。将 genome.fasta 和 inchworm.fasta 输入 PASA，得到用于 trainning 的基因，然后使用 SNAP 进行 training，得到 HMM 文件。
7. Genemark_es hmm file [es.mod]
    适合本物种的 Genemark_es 的 HMM 文件。将 genome.fasta 输入 genemark_es 软件进行自我训练得到的 HMM 文件。
8. rRNA.fa
    rRNA 的序列文件。该文件使用 RNAmmer 对基因组进行分析得到。
 wget http://korflab.ucdavis.edu/Software/snap-2013-02-16.tar.gz && \
 tar zxf snap-2013-02-16.tar.gz && \
 cd snap && \
 make && \
