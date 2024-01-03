#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/CA_NoReg/CA_NoReg$i.sh 
done
