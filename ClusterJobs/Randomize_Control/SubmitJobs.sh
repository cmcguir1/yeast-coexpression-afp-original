#!/usr/bin/sh

<<<<<<< HEAD
for i in {0..11}
=======
for i in {0..3}
>>>>>>> 5ff3177fb48782f38673524226af2c09a7b921c5
do
	qsub data/SummerResearch2022/ClusterJobs/Randomize_Control/Randomize_Control$i.sh 
done
