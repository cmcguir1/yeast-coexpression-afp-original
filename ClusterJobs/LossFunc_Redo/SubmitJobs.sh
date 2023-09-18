#!/usr/bin/sh

for i in {0..5}
do
	qsub data/SummerResearch2022/ClusterJobs/LossFunc_Redo/LossFunc_Redo$i.sh 
done
