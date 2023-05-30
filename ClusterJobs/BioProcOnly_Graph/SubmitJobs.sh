#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/BioProcOnly_Graph/BioProcOnly_Graph$i.sh 
done
