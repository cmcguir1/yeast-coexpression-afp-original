from scipy.stats import kstest, ks_2samp
from scipy import stats
from random import random
import pandas as pd

samp2 = [random() for _ in range(1000)]
samp1 = [random()*0.5 for _ in range(1000)]

# test = ks_2samp(samp1,samp2,alternative='greater')
# print(test)
# test = ks_2samp(samp1,samp2,alternative='less')
# print(test)
# test = ks_2samp(samp1,samp2,alternative='two-sided')
# print(test)
print(kstest(samp1,'uniform',alternative='less'))