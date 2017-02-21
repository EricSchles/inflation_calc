from inflation_calc import CPI
from inflation_calc.predict import main
import pandas as pd
import datetime
import math
try:
    cpi = CPI()
    x = cpi.data["United States"]
    import code
    code.interact(local=locals())
except:
    import code
    code.interact(local=locals())
