#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Heterogeneous_Opt/Heterogeneous_Opt$i.sh 
done
