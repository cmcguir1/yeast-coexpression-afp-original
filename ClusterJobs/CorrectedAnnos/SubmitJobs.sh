#!/usr/bin/sh

for i in {0..1}
do
	qsub data/SummerResearch2022/ClusterJobs/CorrectedAnnos/CorrectedAnnos$i.sh 
done
