#just testing tings

import numpy as np
import pandas as pd

df = pd.DataFrame({"A": [8, 2, 6, 4],
                   "B": [5, 6, 7, 8]})

df_array = df['A'].to_numpy()


print(np.mean(df_array[0:2]))
