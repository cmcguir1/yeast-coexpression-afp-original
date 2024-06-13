import pandas as pd
import numpy as np
from GSEA import GSEA
from multiprocessing import freeze_support


if __name__ == '__main__':
    freeze_support()
    data = pd.read_csv('./Yeast Resources/GSEA_Strunk/Strunk_GeneExpression_log2.csv')
    
    data = data.dropna(subset=['Log2 Fold Change'])
    print(data)

    GSEA(data,'Log2 Fold Change',bpOnly=False,termCutoff=5,commonNames=True,folder='./Yeast Resources/GSEA_Strunk/',name='GSEA')

        
    
