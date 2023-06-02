#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Modern_bioPIXIE_Graph/Modern_bioPIXIE_Graph$i.sh 
done
