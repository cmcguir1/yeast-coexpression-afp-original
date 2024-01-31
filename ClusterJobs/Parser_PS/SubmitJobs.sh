#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/Parser_PS/Parser_PS$i.sh 
done
