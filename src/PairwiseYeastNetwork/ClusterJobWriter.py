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
                       f.write(f'{command} {pythonFilePath}{pythonFile} {arg1[a1]} {arg2[a2]} {arg3[a3]} {arg4[a4]} {arg5[a5]} > ClusterJobs/{JobName}/{JobName}{jobNum}_output.txt')
                       f.close()

                       f = open(f'./ClusterJobs/{JobName}/{JobName}{jobNum}_output.txt','w')
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
# writeJobs('Modern_bioPIXIE','Main3.py')
# writeJobs('Modern_bioPIXIE_Graph_new','Main6.py')
# writeJobs('Cyclic_lr','Main.py')
# writeJobs('MitoOrg_ST','SingleTermMain.py',arg1=['GO:0007005'],arg2=['2000'],arg3=['0','1','2','3'])
# writeJobs('AG_Overfit_lr','Main4.py',arg2=['0.001','0.0001','0.00001'])
# writeJobs('MitoOrg_ST_Graph','Main6.py')
# writeJobs('ST_ParaSearch','SingleTermMain.py',arg1=['GO:0007005'],arg2=['100','500','1000'],arg3=['0.1','0.01','0.001','0.0001'],arg4=['runAll'])
# writeJobs('TestClusterSpeed','Main7.py',arg1=['GO:0007005'],arg2=['2000'],arg3=['0.01'],arg4=['0'],arg5=['50','500'])
# writeJobs('FL_Control','Main6.py',arg2=['FL','CE'])
# writeJobs('LossFunc','Main4.py',arg2=['CCE'])
# writeJobs('UnrelatedNode','Main3.py')
# writeJobs('CE_OnlyPos','Main5.py',arg2=['0.01','0.001'])
# writeJobs('CorrelationDict','Main.py',arg1=[''])
# writeJobs('MemMapTest','Main.py',arg2=['YeastDict_ReCalc2.npy'])
# writeJobs('CorrelationRecalc','Main2.py',arg1=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'])
# writeJobs('LR_ps','Main3.py',arg2=['0.01','0.001','0.0001','0.00001'])
# writeJobs('LossFunc2','Main4.py',arg2=['SM_BCE','SM_MSE','MSE'])
# writeJobs('WCE','Main.py',arg2=['0'])
# writeJobs('FL_ps','Main2.py',arg2=['1','2','5'])
# writeJobs('Modern_OnlyPos','Main3.py')
# writeJobs('OnlyPos_ps','Main6.py',arg2=['0.01','0.001','0.0001'],arg3=['CE','FL'])
# writeJobs('RandomizedLabels_swapGenes','Main2.py')
# writeJobs('Overfit_OnlyPos','Main4.py',arg2=['0.0001','0.00001'])
# writeJobs('Overfit_Unreasonable','Main4.py',arg2=['100000','250000','500000','1000000','25000x5000x5000x5000x5000'])
# writeJobs('Random_SwapGenes','Main2.py',arg2=['200','2000','25000'])
# writeJobs('RandomInputs','Main3.py',arg2=['200','2000','25000'])
# writeJobs('Randomize_Control','Main4.py',arg2=['200','2000','25000'])
# writeJobs('Dropout_OnlyPos','Main4.py',arg2=['0.1','0.3','0.5'])
# writeJobs('BatchSize','Main3.py',arg2=['1','10','50','500'])
# writeJobs('Struct_OnlyPos','Main3.py',arg2=['50','100','100x50','100x50x50x50x50'])
# writeJobs('lr_OnlyPos','Main4.py',arg2=['0.1','0.01','0.001'])

# writeJobs('WeightDecay','Main.py',arg2=['0.1','0.01','0.001','0.0001'])
# writeJobs('Dropout_SmallStruct','Main2.py',arg2=['0.1','0.3','0.5'])
# writeJobs('Batch_SmallStruct','Main3.py',arg2=['1','5','10','50'])
# writeJobs('SmallStruct','Main4.py',arg2=['5','10','20','30'])
# writeJobs('GraphTest','GraphMain.py')
# writeJobs('SmallStruct_WD','Main.py',arg1=['100','50','30','20'],arg2=['0.01','0.001','0.0001'])
# writeJobs('Dropout_Small','Main2.py',arg1=['100','50','30','20'],arg2=['0.1','0.3','0.5'])
# writeJobs('Deep_SmallStruct','Main3.py',arg1=['20x10','15x10','20x10x10x10x10'])
# writeJobs('LossFunc_Redo','Main.py',arg1=['20','100','200'],arg2=['CE','BCE'])
# writeJobs('CE_NegativeNode','Main2.py',arg1=['20','100','200'])
# writeJobs('Opt_Dropout','Main3.py',arg1=['20','100','200'],arg2=['0.1','0.3','0.5'])
# writeJobs('Opt_WeightDecay','Main4.py',arg1=['20','100','200'],arg2=['0.1','0.01','0.001','0.0001'])
# writeJobs('Opt_Dropout+WD','Main3.py',arg1=['20','100'],arg2=['0.1','0.3','0.5'],arg3=['0.001','0.0025','0.005','0.01'])

# writeJobs('Heterogeneous_Baseline_100_Graph','Main.py',arg1=[''])
# writeJobs('Heterogeneous_Baseline_20_Graph','Main2.py',arg1=[''])
# writeJobs('Heterogeneous_Reg_100_Graph','Main3.py',arg1=[''])
# writeJobs('Heterogeneous_Reg_20_Graph','Main4.py',arg1=[''])
# writeJobs('Opt_Net20_WD0.0025_Dropout0.1','Main5.py')
# writeJobs('Opt_Net100_WD0.005_Dropout0.5','Main6.py')
# writeJobs('Opt_Net20_WD0.005_Dropout0.5','Main7.py')
# writeJobs('BCE_20','Main8.py',arg1=[''])
# writeJobs('BCE_100','Main9.py',arg1=[''])
# writeJobs('CE_100','Main10.py',arg1=[''])
# writeJobs('CE_20','Main11.py',arg1=[''])
# writeJobs('Heterogenous_BCE_Reg_20','Main12.py',arg1=[''])
# writeJobs('Heterogenous_BCE_Baseline_20','Main13.py',arg1=[''])

# writeJobs('Heterogeneous_Baseline_100_Graph','Main.py')
# writeJobs('Heterogeneous_Baseline_20_Graph','Main2.py',arg1=[''])
# writeJobs('Heterogeneous_Reg_100_Graph','Main3.py')
# writeJobs('Heterogeneous_Reg_20_Graph','Main4.py',arg1=[''])
# writeJobs('Opt_Net20_WD0.0025_Dropout0.1','Main5.py')
# writeJobs('Opt_Net100_WD0.005_Dropout0.5','Main6.py')
# writeJobs('Opt_Net20_WD0.005_Dropout0.5','Main7.py')
# writeJobs('BCE_20','Main8.py',arg1=[''])
# writeJobs('BCE_100','Main9.py',arg1=[''])
# writeJobs('CE_100','Main10.py',arg1=[''])
# writeJobs('CE_20','Main11.py',arg1=[''])
# writeJobs('Heterogenous_BCE_Reg_20','Main12.py',arg1=[''])
# writeJobs('Heterogenous_BCE_Baseline_20','Main13.py',arg1=[''])


# writeJobs('Heterogeneous_Opt','Main8.py',arg1=['20','100'])
# writeJobs('Heterogeneous_Opt_Baseline','Main9.py',arg1=['20','100'])

# writeJobs('Heterogenous_BCE_Reg','Main8.py',arg1=['20','100'])
# writeJobs('Heterogenous_BCE_Baseline','Main9.py',arg1=['20','100'])

# writeJobs('AllSingleTerms_20','AllSingleTerms.py',arg1=list(range(30,54)),arg2=['20'])
writeJobs('AllSingleTerms_100','AllSingleTerms.py',arg1=list(range(0,54)),arg2=['100'])


