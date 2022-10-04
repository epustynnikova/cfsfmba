#!/bin/sh
cd data
mkdir ref -p
tar -xvf GRCh38.d1.vd1.fa.tar.gz -C ref
cd ref
faidx --split-files GRCh38.d1.vd1.fa
