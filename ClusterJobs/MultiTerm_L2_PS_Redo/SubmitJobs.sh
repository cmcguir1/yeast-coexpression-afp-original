#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_L2_PS_Redo/MultiTerm_L2_PS_Redo$i.sh 
done
