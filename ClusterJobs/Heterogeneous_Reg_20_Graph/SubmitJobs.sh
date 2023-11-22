#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Heterogeneous_Reg_20_Graph/Heterogeneous_Reg_20_Graph$i.sh 
done
