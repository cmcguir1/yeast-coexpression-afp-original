#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/MolFunc_May-22-2023/MolFunc$i.sh
done
