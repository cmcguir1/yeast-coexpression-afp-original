#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/Opt_Net100_WD0.005_Dropout0.5/Opt_Net100_WD0.005_Dropout0.5$i.sh 
done
