#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/Parser_BioProc_nonLeaves/Parser_BioProc_nonLeaves$i.sh 
done
