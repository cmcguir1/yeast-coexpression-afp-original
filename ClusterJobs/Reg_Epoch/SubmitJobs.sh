#!/usr/bin/sh

for i in {0..4}
do
	qsub data/SummerResearch2022/ClusterJobs/Reg_Epoch/Reg_Epoch$i.sh 
done
