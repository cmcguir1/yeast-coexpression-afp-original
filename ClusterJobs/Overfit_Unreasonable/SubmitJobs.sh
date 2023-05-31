#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Overfit_Unreasonable/Overfit_Unreasonable$i.sh 
done
