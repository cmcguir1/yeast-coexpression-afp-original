#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/AG_Overfit_lr/AG_Overfit_lr$i.sh 
done
