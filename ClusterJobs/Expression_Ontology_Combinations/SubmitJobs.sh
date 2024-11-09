#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Expression_Ontology_Combinations/Expression_Ontology_Combinations$i.sh 
done
