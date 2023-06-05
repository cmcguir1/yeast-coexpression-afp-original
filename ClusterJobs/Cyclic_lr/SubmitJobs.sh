#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Cyclic_lr/Cyclic_lr$i.sh 
done
