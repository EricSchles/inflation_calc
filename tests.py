from inflation_calc import CPI
from inflation_calc.predict import predict, dict_to_dataframe
import pandas as pd
import datetime
import math
try:
    cpi = CPI()
    x= predict(cpi.data["United States"], 5)
    import code
    code.interact(local=locals())
except:
    import code
    code.interact(local=locals())
