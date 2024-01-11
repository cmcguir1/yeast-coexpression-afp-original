#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/CorrectedAnnos_Hetero/CorrectedAnnos_Hetero$i.sh 
done
