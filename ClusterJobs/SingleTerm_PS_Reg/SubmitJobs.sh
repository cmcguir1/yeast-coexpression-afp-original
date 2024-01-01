#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/SingleTerm_PS_Reg/SingleTerm_PS_Reg$i.sh 
done
