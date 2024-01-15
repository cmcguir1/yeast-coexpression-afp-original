#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/Folds_bce_Original_GeneExp/Folds_bce_Original_GeneExp$i.sh 
done
