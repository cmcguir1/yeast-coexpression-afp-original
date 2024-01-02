#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/MitoInheritance_Graph/MitoInheritance_Graph$i.sh 
done
