#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/Modern_Paper/Modern_Paper$i.sh 
done
