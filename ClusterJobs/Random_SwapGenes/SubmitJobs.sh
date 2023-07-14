#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Random_SwapGenes/Random_SwapGenes$i.sh 
done
