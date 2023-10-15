#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Opt_Net20_WD0.005_Dropout0.5/Opt_Net20_WD0.005_Dropout0.5$i.sh 
done
