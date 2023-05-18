import sys

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

leaves = getLeaves(10,cellComp=False,molFunc=False)
print(len(leaves))