#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Modern_bioPIXIE_Graph_new/Modern_bioPIXIE_Graph_new$i.sh 
done
