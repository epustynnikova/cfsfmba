#!/bin/sh
tail -n +1 data/FP_SNPs.txt | grep -v -P "\t23\t" |  awk '{ print "chr" $2 "\t" $4 "\trs" $1 "\t" $5 "\t" $6}' > data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv
