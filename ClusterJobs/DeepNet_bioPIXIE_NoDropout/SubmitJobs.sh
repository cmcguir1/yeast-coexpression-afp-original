#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/DeepNet_bioPIXIE_NoDropout/DeepNet_bioPIXIE_NoDropout$i.sh 
done
