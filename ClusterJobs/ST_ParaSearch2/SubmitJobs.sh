#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/ST_ParaSearch2/ST_ParaSearch2$i.sh 
done
