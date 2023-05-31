#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/DeepNet_bioPIXIE_Dropout/DeepNet_bioPIXIE_Dropout$i.sh 
done
