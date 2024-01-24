#!/usr/bin/sh

for i in {0..14}
do
	qsub data/SummerResearch2022/ClusterJobs/Batch_PS/Batch_PS$i.sh 
done
