#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/ST_MitoOrg/ST_MitoOrg$i.sh 
done
