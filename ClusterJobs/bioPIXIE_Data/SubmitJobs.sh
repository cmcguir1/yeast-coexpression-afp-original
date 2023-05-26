#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/bioPIXIE_Data/bioPIXIE_Data$i.sh 
done
