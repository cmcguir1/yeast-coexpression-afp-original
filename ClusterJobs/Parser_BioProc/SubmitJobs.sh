#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/Parser_BioProc/Parser_BioProc$i.sh 
done
