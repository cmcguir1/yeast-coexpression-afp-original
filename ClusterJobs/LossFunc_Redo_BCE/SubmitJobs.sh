#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/LossFunc_Redo_BCE/LossFunc_Redo_BCE$i.sh 
done
