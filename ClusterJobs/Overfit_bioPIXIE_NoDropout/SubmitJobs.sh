#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Overfit_bioPIXIE_NoDropout/Overfit_bioPIXIE_NoDropout$i.sh 
done
