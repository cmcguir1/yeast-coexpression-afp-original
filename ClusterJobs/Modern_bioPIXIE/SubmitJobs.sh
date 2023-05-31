#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Modern_bioPIXIE/Modern_bioPIXIE$i.sh 
done
