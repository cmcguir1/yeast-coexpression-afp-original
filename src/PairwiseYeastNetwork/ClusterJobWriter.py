import os
import sys
from datetime import date

def writeJobs(JobName,pythonFile,arg1=['0','1','2','3'],arg2=None,arg3=None,arg4=None,arg5=None,command='/data/hibbslab/anaconda3/bin/python',pythonFilePath='src/PairwiseYeastNetwork/'):
    if arg1 == None:
        arg1_range = range(1)
        arg1 = ['']
    else:
        arg1_range = range(len(arg1))
        

    if arg2 == None:
        arg2_range = range(1)
        arg2 = ['']
    else:
        arg2_range = range(len(arg2))
        

    if arg3 == None:
        arg3_range = range(1)
        arg3 = ['']
    else:
        arg3_range = range(len(arg3))
        

    if arg4 == None:
        arg4_range = range(1)
        arg4 = ['']
    else:
        arg4_range = range(len(arg4))
        

    if arg5 == None:
        arg5_range = range(1)
        arg5 = ['']
    else:
        arg5_range = range(len(arg5))
        

    today = date.today()
    dateStr = today.strftime("%b-%d-%Y")
    
    if not os.path.exists(f'./ClusterJobs/{JobName}_{dateStr}'):
        os.makedirs(f'./ClusterJobs/{JobName}_{dateStr}')
    
    

    jobNum = 0
    for a5 in arg5_range:
        for a4 in arg4_range:
            for a3 in arg3_range:
                for a2 in arg2_range:
                    for a1 in arg1_range:
                       print(f'./ClusterJobs/{JobName}_{dateStr}/{JobName}{jobNum}.sh')
                       f = open(f'./ClusterJobs/{JobName}_{dateStr}/{JobName}{jobNum}.sh','w')
                       f.write('#!/usr/bin/sh\n\n')
                       f.write(f'## Job Created {dateStr}\n\n')
                       f.write('##Place PBS directives here\n')
                       f.write(f'#PBS -N {JobName}\n')
                       f.write('#PBS -l nodes=1:ppn=36\n')
                       f.write('#PBS -l walltime=168:00:00\n')
                       f.write('#PBS -M cmcguir1@trinity.edu\n')
                       f.write('#PBS -m ae\n\n')
                       f.write('cd data/SummerResearch2022\n\n')
                       f.write(f'{command} {pythonFilePath}{pythonFile} {arg1[a1]} {arg2[a2]} {arg3[a3]} {arg4[a4]} {arg5[a5]}')
                       f.close()

                       jobNum += 1
    f = open(f'./ClusterJobs/{JobName}_{dateStr}/{JobName}_SubmitJobs.sh','w')
    f.write('#!/usr/bin/sh\n\n')
    f.write('for i in {0..%s}\n' %f'{jobNum-1}')
    f.write(f'do\n\tqsub data/SummerResearch2022/ClusterJobs/{JobName}_{dateStr}/{JobName}$i.sh\ndone\n')

# writeJobs('MolFunc','Main6.py',arg2=['2000','25000'])
writeJobs('Test','TestMain.py')



