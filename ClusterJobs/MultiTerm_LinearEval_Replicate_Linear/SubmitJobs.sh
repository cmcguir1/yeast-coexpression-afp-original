#!/usr/bin/sh

for i in {0..1}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_LinearEval_Replicate_Linear/MultiTerm_LinearEval_Replicate_Linear$i.sh 
done
