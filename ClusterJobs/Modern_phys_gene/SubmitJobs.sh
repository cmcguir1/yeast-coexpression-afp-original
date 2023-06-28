#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Modern_phys_gene/Modern_phys_gene$i.sh 
done
