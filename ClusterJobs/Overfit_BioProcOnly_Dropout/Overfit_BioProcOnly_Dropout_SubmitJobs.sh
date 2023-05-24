#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Overfit_BioProcOnly_Dropout/Overfit_BioProcOnly_Dropout$i.sh 
done
