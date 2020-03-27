import scipy.io as spio
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

parquet = pd.read_parquet('MOSFET.parquet')
#print(type(parquet))