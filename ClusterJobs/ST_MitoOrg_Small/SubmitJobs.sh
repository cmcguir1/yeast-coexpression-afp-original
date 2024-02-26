#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/ST_MitoOrg_Small/ST_MitoOrg_Small$i.sh 
done
