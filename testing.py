#just testing tings

import numpy as np
import pandas as pd

df = pd.DataFrame({4: [8, 2, 6, 4],
                   5: [5, 6, 7, 8]})

test_array = [4,5]
for i in test_array:
    print(df[i][1])

