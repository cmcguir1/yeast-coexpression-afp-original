#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/AllTerms+Localization/AllTerms+Localization$i.sh &> data/SummerResearch2022/ClusterJobs/AllTerms+Localization/AllTerms+Localization$i_output.txt
done
