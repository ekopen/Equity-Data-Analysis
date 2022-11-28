import numpy as np
import pandas as pd

df = pd.DataFrame({"A": [1, 2, 3, 4],
                   "B": [5, 6, 7, 8]})

print(df.loc['A'])