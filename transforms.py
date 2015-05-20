import numpy as np
import pandas as pd

from sklearn.preprocessing import normalize, StandardScaler
from sklearn.cross_validation import train_test_split, KFold

from itertools import combinations

class transforms(object):
    def __init__(self):
        print 'transforms'
    #stem

