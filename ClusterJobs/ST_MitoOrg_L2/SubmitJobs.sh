#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/ST_MitoOrg_L2/ST_MitoOrg_L2$i.sh 
done
