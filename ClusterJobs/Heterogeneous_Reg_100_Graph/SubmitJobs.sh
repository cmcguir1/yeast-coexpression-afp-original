#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/Heterogeneous_Reg_100_Graph/Heterogeneous_Reg_100_Graph$i.sh 
done
