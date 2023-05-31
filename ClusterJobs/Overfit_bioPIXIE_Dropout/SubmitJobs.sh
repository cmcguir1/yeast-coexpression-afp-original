#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Overfit_bioPIXIE_Dropout/Overfit_bioPIXIE_Dropout$i.sh 
done
