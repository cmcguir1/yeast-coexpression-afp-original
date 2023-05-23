#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/BioProc+Local_Graph/BioProc+Local_Graph$i.sh 
done
