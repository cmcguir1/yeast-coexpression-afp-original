#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/bioPIXIE_Data_Graph/bioPIXIE_Data_Graph$i.sh 
done
