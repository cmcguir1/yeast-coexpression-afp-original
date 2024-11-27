import os
import sys
from datetime import date
import shutil

def writeJobs(JobName,pythonFile,node=False,arg1=['0','1','2','3'],arg2=None,arg3=None,arg4=None,arg5=None,argNames=[],command='/data/hibbslab/anaconda3/bin/python',pythonFilePath='src/PairwiseYeastNetwork/'):
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

    while len(argNames) < 5:
        argNames.append('')
    n1, n2, n3, n4, n5 = argNames
    

    today = date.today()
    dateStr = today.strftime("%b-%d-%Y")
    
    if not os.path.exists(f'./ClusterJobs/{JobName}'):
        os.makedirs(f'./ClusterJobs/{JobName}')

    # Nodes with high memory errors: 38,39,40,41
    # Nodes that are down: 0,1,2,5,11,35,37
    nodes = [3,4,6,7,8,9,10,12,13,14,15,116,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,42]

    jobNum = 0
    nodeNum = 0
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
                       f.write(f'#PBS -N {JobName}{"" if arg1[a1] == "" else f"_{n1}{arg1[a1]}"}{"" if arg2[a2] == "" else f"_{n2}{arg2[a2]}"}{"" if arg3[a3] == "" else f"_{n3}{arg3[a3]}"}{"" if arg4[a4] == "" else f"_{n4}{arg4[a4]}"}{"" if arg5[a5] == "" else f"_{n5}{arg5[a5]}"}\n')
                       if node:
                           f.write(f'#PBS -l nodes=n{nodes[nodeNum]}:ppn=36\n')
                       else:
                           f.write(f'#PBS -l nodes=1:ppn=36\n')
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
                       nodeNum = (nodeNum + 1) % len(nodes)
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

# writeJobs('AllSingleTerms_20_CT','AllSingleTerms.py',arg1=list(range(0,54)),arg2=['20'],node=True)
# writeJobs('AllSingleTerms_100','AllSingleTerms.py',arg1=list(range(10,54)),arg2=['100'])
# writeJobs('TestSpecificNode','TestArea.py',arg1=[''])
# writeJobs('MitoInheritance','MitoInheritance.py',arg2=['20'],arg1=['0'])
# writeJobs('AllSingleTerms_100_Leftovers','AllSingleTerms_Leftovers.py',arg1=range(0,15),arg2=['100'])
# writeJobs('BCE_20_Sigmoid','GraphMain.py',arg1=['True','False'])
# writeJobs('Paper_BCE_20','Main.py',arg1=['20','100'])
# writeJobs('Paper_BCE_20_Reg','Main2.py',arg1=['20','100'],arg2=[0.1,0.5])
# writeJobs('Paper_BCE_20_Hetero','Main3.py',arg1=['20','100','200'],arg2=[0.1,0.5])
# writeJobs('Paper_BCE_20_Hetero_Reg','Main4.py',arg1=['20','100','200'],arg2=[0.1,0.5])
# writeJobs('MitoInheritance_Graph','MitoInheritance.py',arg2=['20'],arg1=['0'])
    
# writeJobs('BCE_Reg_PS','Main5.py',arg1=[0,0.0001,0.001,0.01],arg2=[0,0.1,0.5])
# writeJobs('SingleTerm_PS_Struct','Main6.py',arg2=['5','10'])
# writeJobs('SingleTerm_PS_Reg','Main7.py',arg1=[0,0.0001,0.001,0.01],arg2=[0,0.1,0.5])

# writeJobs('Paper_BCE_Graph','Main.py',arg1=['20','100'],arg2=[0,1,2,3])
# writeJobs('Paper_BCE_Hetero_Graph','Main.py',arg1=['20','100'],arg2=[0,1,2,3])
# writeJobs('MitoInheritance_Graph','MitoInheritance.py',arg2=['20'],arg1=['0'])
# writeJobs('CorrectedAnnos','Main.py',arg1=['20','100'],arg2=[0,1,2,3])
# writeJobs('CorrectedAnnos_Hetero','Main3.py',arg1=['20','100'],arg2=[0,1,2,3])
# writeJobs('Reg_Epoch','Main2.py',arg1=[0,10000,25000,50000,100000])
# writeJobs('CA_WD','Main2.py')
# writeJobs('CA_Dropout','Main4.py',arg2=[0.1,0.01,0.001])

# writeJobs('CA_NoReg','Main2.py')

# writeJobs('CorrectedAnnos','Main5.py',arg1=['20','100'])
# writeJobs('CorrectedAnnos_Hetero','Main6.py',arg1=['20','100'])
# writeJobs('MitoInheritance_Graph','MitoInheritance.py',arg2=['20'],arg1=[0])
# writeJobs('Modern_Paper','Main2.py',arg1=['20','100','200'])
# writeJobs('Folds_bce_Original_GeneExp','Main.py',arg1=['100'],arg2=[0])
# writeJobs('Folds_bce_Original_Hetero','Main2.py',arg1=['100'],arg2=[0])
# writeJobs('Folds_bce_Modern_GeneExp','Main3.py',arg1=['100'],arg2=[0])
# writeJobs('Folds_bce_Modern_Hetero','Main4.py',arg1=['100'],arg2=[0])
# writeJobs('Parser_BioProc','Main.py',arg1=[0])
# writeJobs('Parser_BioProc_nonLeaves','Main2.py',arg1=[0])
# writeJobs('Parser_AllRoots','Main3.py',arg1=[0])
# writeJobs('Parser_AllRoots_nonLeaves','Main4.py',arg1=[0])

# writeJobs('Batch_PS','Main5.py',arg1=[50,500],arg2=[1,2,3,4,5])
# writeJobs('SmallestCommonAncestor','Main10.py',arg1=[''])
# writeJobs('HardNegatives','Main9.py',arg1=[0])
# writeJobs('EasyNegatives','Main10.py',arg1=[0])
# writeJobs('Parser_PS','Main.py',arg2=['20','100','200','200x100'],arg1=[0])
# writeJobs('AllTermLoss','Main2.py')
# writeJobs('PosWeights_Control','Main3.py',arg1=[0])
# writeJobs('PosWeights','Main4.py',arg2=[0.1,1,10],arg1=[0])
# writeJobs('ST_MitoOrg_Small','Main3.py',arg2=['1','3','5','10'],arg1=[0])
# writeJobs('ST_MitoOrg_L2','Main5.py',arg2=[0.1,0.01,0.005],arg1=[0])
# writeJobs('Net_bcm','Main4.py',arg2=['20','100','200x100','500','500x200x100'],arg1=[0])
# writeJobs('SingleTerm_2.28','Main6.py')
# writeJobs('ST_MitoOrg_L2_PS','Main7.py',arg1=[0.1,0.5,1],arg2=['100','200','500','500x200x100x100'])
# writeJobs('MultiTerm_L2_PS','Main8.py',arg2=[0.1,0.01],arg3=['200','500','500x100x100x100'])

# writeJobs('MultiTerm_L2_PS_1','Main8.py',arg2=[0.1],arg3=['200'],arg1=[0])
# writeJobs('MultiTerm_L2_PS_2','Main8.py',arg2=[0.1,0.01],arg3=['500x100x100x100'],arg1=[0])
# writeJobs('MultiTerm_L2_PS_Redo','Main8.py',arg2=[0.05,0.01,0.005,0.001],arg3=['100','100x50x50'])
# writeJobs('MultiTerm_L2_PS_4','Main8.py',arg2=[0.00005,0.00001],arg3=['100','100x50x50'])
# writeJobs('MultiTerm_Struct_PS','Main9.py',arg2=['100x50x50','200x100','200','20'])
# writeJobs('MultiTerm_Struct_PS','Main9.py',arg2=['200x100','20'],arg1=[0])
# writeJobs('ST_MitoOrg_L2','Main5.py',arg2=[0.1],arg1=[0])
    
# writeJobs('ST_PS_Term','Main5.py',arg1=['GO:0007005','GO:0006260','GO:0006869'],arg2=[0.05,0.1,0.2])
# writeJobs('MultiTerm_Struct_PS','Main9.py',arg2=['500x200x100','500x200'])
# writeJobs('MultiTerm_Struct_PS','Main9.py',arg2=['500x200x100'],arg1=[0])

# writeJobs('MultiTerm_L2_PS_Redo','Main8.py',arg2=[0,0.0001,0.00001,0.000001],arg3=['500x200x100'])
# writeJobs('ST_PS_Term','Main5.py',arg1=['GO:0006486','GO:0015031'],arg2=[0.5,0.1,0.01])

# writeJobs('MultiTerm_L2_PS_Redo','Main8.py',arg2=[0],arg3=['500x200x100'],arg1=[0])
# writeJobs('ST_PS_Term','Main5.py',arg1=['GO:0006486','GO:0015031',],arg2=[0.5,0.1,0.01])
# writeJobs('ST_PS_Term_MitoOrg','Main4.py',arg1=['GO:0007005','GO:0006486','GO:0015031'],arg2=[0.5,0.1,0.01])

# writeJobs('MemMap_Debug','Main8.py',arg2=[0,0.0001,0.00001,0.000001],arg3=['500x200x100'],arg1=[0])

# writeJobs('MultiTerm_LinearEval','Main.py',arg1=[0])
# writeJobs('MemMap_StressTest_Floats','TestMain3.py',arg1=['../Cluster_'])
# writeJobs('MemMap_StressTest_Pairs','TestMain2.py',arg1=['../Cluster_'])

# writeJobs('MultiTerm_LinearEval_Replicate_Linear','Main2.py',arg2=['20','200'],arg3=[0],arg1=[0])
# writeJobs('MultiTerm_LinearEval_Replicate_Parallel','Main3.py',arg2=['20','200'],arg3=[1],arg1=[0])

# writeJobs('MultiTerm_NetStruct_PS','Main.py',arg2=['200','500x200x100','1000'],arg3=[0],arg1=[0])
# writeJobs('MultiTerm_NetStruct_PS_Orignal','Main.py',arg2=['500x200x100'],arg3=[0],arg1=[0])
# writeJobs('MultiTerm_NetStruct_PS_Modern','Main2.py',arg2=['500x200x100'],arg3=[0],arg1=[0])
# writeJobs('MultiTerm_NetStruct_Replicates_Original','Main3.py',arg2=['500x200x100'],arg3=[1,2,3],arg1=[0])
# writeJobs('MultiTerm_NetStruct_Replicates_Modern','Main4.py',arg2=['500x200x100'],arg3=[1,2,3],arg1=[0])
# writeJobs('MultiTerm_Modern_NetStruct','Main.py',arg2=['500x200x100','1000','1000x500x200'],arg3=[0],arg1=[0])
# writeJobs('GSEA','GSEA.py',arg1=['NN','SPELL','MEFIT','bioPIXIE'])
# writeJobs('GSEA_subsets','GSEA.py',arg1=['NN','SPELL','MEFIT','bioPIXIE'])
# writeJobs('GSEA_Strunk','GSEA_strunk.py',arg1=[0.5,1,2,5])
# writeJobs('MultiTerm_Modern_NetStruct','Main.py',arg2=['1000x500x200'],arg3=[0],arg1=[0])
# writeJobs('MultiTerm_NetStruct_PS','Main2.py',arg2=['500x200x100'],arg3=[0],arg1=[0])
# writeJobs('ZLPR_BCE_Comparison','Main3.py',arg2=['ZLPR','BCE'],arg1=[0,1,2,3])
# writeJobs('ConsistencyReplicates_DiffFold','Main5.py',arg2=[0,1,2,3,4],arg1=[0])
# writeJobs('ConsistencyReplicates_SameFold','Main6.py',arg2=[0,1,2,3,4],arg1=[0])
# writeJobs('ConsistencyReplicates_DiffFold','Main5.py',arg2=range(5,20),arg1=[0])
# writeJobs('ConsistencyReplicates_SameFold','Main6.py',arg2=range(5,20),arg1=[0])
# writeJobs('OverfittingTest','Main3.py',arg2=['500x200x100','200','20','80x80x80'],arg3=[50000,300000])
writeJobs('OverfittingTest2','Main4.py',arg2=['80','80x80x80','20x20x20'],arg1=[0])
# writeJobs('OverfittingTest_Graph','Main4.py',arg2=['20','80','80x80x80','20x20x20'],arg3=[300000,600000])
# writeJobs('Expression_Ontology_Combinations','Main7.py',arg2=['2007','2022'],arg3=['2007','2022'],arg4=['500x200x100'])
# writeJobs('CutoffSize','Main8.py',arg2=[19,20],arg3=['20x20x20','80x80x80'])

