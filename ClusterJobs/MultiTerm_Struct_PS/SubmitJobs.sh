#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_Struct_PS/MultiTerm_Struct_PS$i.sh 
done
