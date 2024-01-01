#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/BCE_Reg_PS/BCE_Reg_PS$i.sh 
done
