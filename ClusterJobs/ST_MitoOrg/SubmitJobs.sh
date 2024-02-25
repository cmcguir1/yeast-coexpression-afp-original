#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/ST_MitoOrg/ST_MitoOrg$i.sh 
done
