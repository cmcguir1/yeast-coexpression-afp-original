#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/LearningRate/LearningRate$i.sh 
done
