#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/Opt_Net20_WD0.0025_Dropout0.1/Opt_Net20_WD0.0025_Dropout0.1$i.sh 
done
