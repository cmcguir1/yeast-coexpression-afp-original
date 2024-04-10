#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/ST_PS_Term_MitoOrg/ST_PS_Term_MitoOrg$i.sh 
done
