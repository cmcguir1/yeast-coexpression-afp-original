#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/SingleTerm_PS_Struct/SingleTerm_PS_Struct$i.sh 
done
