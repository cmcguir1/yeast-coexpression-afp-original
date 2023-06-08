import os
import sys
from datetime import date
import shutil

def writeJobs(JobName,pythonFile,arg1=['0','1','2','3'],arg2=None,arg3=None,arg4=None,arg5=None,command='/data/hibbslab/anaconda3/bin/python',pythonFilePath='src/PairwiseYeastNetwork/'):
    argRanges = []
    args = []
    for arg in [arg1,arg2,arg3,arg4,arg5]:
        if arg == None:
            argRanges.append(range(1))
            args.append([''])
        else:
            argRanges.append(range(len(arg)))
            args.append(arg)
    
    arg1, arg2, arg3, arg4, arg5 = args
    

    today = date.today()
    dateStr = today.strftime("%b-%d-%Y")
    
    if not os.path.exists(f'./ClusterJobs/{JobName}'):
        os.makedirs(f'./ClusterJobs/{JobName}')
    
    

    jobNum = 0
    for a5 in argRanges[4]:
        for a4 in argRanges[3]:
            for a3 in argRanges[2]:
                for a2 in argRanges[1]:
                    for a1 in argRanges[0]:
                       print(f'./ClusterJobs/{JobName}/{JobName}{jobNum}.sh')
                       f = open(f'./ClusterJobs/{JobName}/{JobName}{jobNum}.sh','w')
                       f.write('#!/usr/bin/sh\n\n')
                       f.write(f'## Job Created {dateStr}\n\n')
                       f.write('##Place PBS directives here\n')
                       f.write(f'#PBS -N {JobName}\n')
                       f.write('#PBS -l nodes=1:ppn=36\n')
                       f.write('#PBS -l walltime=168:00:00\n')
                       f.write('#PBS -M cmcguir1@trinity.edu\n')
                       f.write('#PBS -m ae\n\n')
                       f.write('cd data/SummerResearch2022\n\n')
                       #f.write(f'touch data/SummerResearch2022/ClusterJobs/{JobName}/{JobName}{jobNum}_output.txt\n')
                       #f.write(f'{command} {pythonFilePath}{pythonFile} {arg1[a1]} {arg2[a2]} {arg3[a3]} {arg4[a4]} {arg5[a5]} > data/SummerResearch2022/ClusterJobs/{JobName}/{JobName}{jobNum}_output.txt')
                       f.write(f'{command} {pythonFilePath}{pythonFile} {arg1[a1]} {arg2[a2]} {arg3[a3]} {arg4[a4]} {arg5[a5]}')
                       f.close()

                       jobNum += 1
    f = open(f'./ClusterJobs/{JobName}/SubmitJobs.sh','w')
    f.write('#!/usr/bin/sh\n\n')
    f.write('for i in {0..%s}\n' %f'{jobNum-1}')
    f.write(f'do\n\tqsub data/SummerResearch2022/ClusterJobs/{JobName}/{JobName}$i.sh \ndone\n')

    shutil.copy(f'{pythonFilePath}{pythonFile}',f'./ClusterJobs/{JobName}/{pythonFile}')

    # Make it so that you redirect standard out and error to a file using &>
    f = open(f'./ClusterJobs/{JobName}/JobInformation.txt','w')
    f.write(f'{dateStr}\n')
    f.close()


# writeJobs('BioProc+LocalizationData','GraphMain.py',arg2=['25000','2000'])
# writeJobs('BioProcOnly_Graph','Main.py',arg2=['25000'])
# writeJobs('bioPIXIE_Data_Graph','Main2.py',arg2=['25000'])
# writeJobs('bioPIXIE_Data','Main2.py',arg2=['2000','25000'])
# writeJobs('Overfit_BioProcOnly_Dropout','Main7.py')
# writeJobs('DeepNet_bioPIXIE_NoDropout','Main3.py')
# writeJobs('DeepNet_bioPIXIE_Dropout','Main4.py')
# writeJobs('Overfit_Unreasonable','Main3.py')
# writeJobs('Modern_bioPIXIE','Main4.py')
# writeJobs('Modern_bioPIXIE_Graph','GraphMain.py')
# writeJobs('Cyclic_lr','Main.py')
writeJobs('MitoOrg_ST','SingleTermMain.py',arg1=['GO:0007005'],arg2=['2000'],arg3=['0','1','2','3'])


