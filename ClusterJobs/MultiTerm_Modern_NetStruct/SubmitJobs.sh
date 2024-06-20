#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_Modern_NetStruct/MultiTerm_Modern_NetStruct$i.sh 
done
