#!/usr/bin/sh

for i in {0..5}
do
	qsub data/SummerResearch2022/ClusterJobs/ST_PS_Term/ST_PS_Term$i.sh 
done
