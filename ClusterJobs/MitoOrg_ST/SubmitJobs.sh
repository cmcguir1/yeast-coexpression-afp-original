#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/MitoOrg_ST/MitoOrg_ST$i.sh 
done
