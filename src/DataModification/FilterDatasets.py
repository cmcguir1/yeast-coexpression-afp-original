from multiprocessing.reduction import duplicate
import shutil
import numpy
import glob
import pandas as pd


files = [file for file in glob.glob('./Yeast Resources/Datasets/All Spell/all spell datasets/**/*')]
#print(files)
original = pd.read_csv('./Yeast Resources/sce_original_arrays_info.txt',sep='\t',encoding="unicode_escape").to_numpy()

# duplicates = set()
# for i in range(len(files)):
#     for j in range(len(files[i+1:])):
#         if files[i][files[i].find('\\')+2:files[i].find('_')] in files[j]:
#             duplicates.add(files[i])
# print(duplicates)
# print(len(duplicates))

#Anderson, Aragon, Boer, Brauer, Carter, Daran-Lap, Fry, Gardner
            


filtered = set()
inFiles = []
for file in files:
    for name in original[:,0]:
        #if name[:name.find('0')] in file or name[:name.find('1')] in file or name[:name.find('9')] in file:
        if name[:name.find('.')] in file:
            filtered.add(file)
            inFiles.append(name)
# for file in files:
#     for name in list(set(original[:,0]) - set(inFiles)):
#         if name[:name.find('0')] in file or name[:name.find('1')] in file or name[:name.find('9')] in file:
#         #if name[:name.find('.')] in file:
#             filtered.add(file)
#             inFiles.append(name)

print(f'All Files: {len(files)}')
print(f'Filtered Files: {len(filtered)}')
print(set(original[:,0]) - set(inFiles))

for file in filtered:
    dest = f"{file[:file.find('all spell datasets')-1]}/original/" + file[file.rfind('\\')+1:]
    #shutil.copy(file,dest)


#'./Yeast Resources/Datasets/All Spell/all spell datasets\\Abbott_2008_PMID_18676708\\GSE10066_setA_family.pcl'


