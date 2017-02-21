import pandas as pd
import math
import datetime
import statsmodels.api as sm
import statistics
from functools import partial
import code
from scipy.optimize import brute
import json

# this comes from here:
# http://stackoverflow.com/questions/22770352/auto-arima-equivalent-for-python
def objective_function(data, order):
    return sm.tsa.ARIMA(data, order).fit(disp=0).aic

def brute_search(data):
    print("got here with no errors")
    obj_func = partial(objective_function, data)
    # Back in graduate school professor Lecun said in class that ARIMA models
    # typically only need a max parameter of 5, so I doubled it just in case.
    upper_bound_AR = 10
    upper_bound_I = 10
    upper_bound_MA = 10
    grid_not_found = True
    print("got to while loop")
    while grid_not_found:
        try:
            if upper_bound_AR < 0 or upper_bound_I < 0 or upper_bound_MA < 0:
                grid_not_found = False
            grid = (
                slice(1, upper_bound_AR, 1),
                slice(1, upper_bound_I, 1),
                slice(1, upper_bound_MA, 1)
            )
            order = brute(obj_func, grid, finish=None)
            return order

        except Exception as e:
            error_string = str(e)
            if "MA" in error_string:
                upper_bound_MA -= 1
            elif "AR" in error_string:
                upper_bound_AR -= 1
            else:
                upper_bound_I -= 1

    # assuming we don't ever hit a reasonable set of upper_bounds,
    # it's pretty safe to assume this will work
    try:
        grid = (
            slice(1, 2, 1),
            slice(1, 2, 1),
            slice(1, 2, 1)
        )
        order = brute(obj_func, grid, finish=None)
        return order

    except:  # however we don't always meet invertibility conditions
        # Here we explicitly test for a single MA
        # or AR process being a better fit
        # If either has a lower (better) aic score we return that model order
        try:
            model_ar_one = sm.tsa.ARIMA(data, (1, 0, 0)).fit(disp=0)
            model_ma_one = sm.tsa.ARIMA(data, (0, 0, 1)).fit(disp=0)
        except:
            return None
        if model_ar_one.aic < model_ma_one.aic:
            return (1, 0, 0)
        else:
            return (0, 0, 1)

def dict_to_dataframe(data):
    df = pd.DataFrame()
    for key in data.keys():
        df = df.append({"year":key, "cpi":data[key]}, ignore_index=True)
    df["year"] = df.apply(lambda x: datetime.date(year=int(x["year"]),month=1,day=1), axis=1)
    df["year"] = pd.to_datetime(df["year"])
    df = df.set_index("year")
    df.sort_index(inplace=True)
    return df

def predict(df,steps):
    print("started function")
    start = df.index[0].year
    end = df.index[-1].year
    years_captured = [idx.year for idx in df.index]
    years_inclusive = [elem for elem in range(start, end+1)]
    s = df.T.squeeze()
    for year in years_inclusive:
        if not year in years_captured:
            s = s.set_value(datetime.datetime(year=year,month=1,day=1),math.nan)
    s.sort_index(inplace=True)
    s = s.interpolate()
    data = s.to_frame()
    print("loaded data")
    model_order = brute_search(data)
    model_order = tuple([int(elem) for elem in model_order])
    print("found model order")
    model = sm.tsa.ARIMA(data, model_order).fit(disp=0)
    print("fit model")
    return model.forecast(steps=steps)[0], end

def main(data, steps):
    df = dict_to_dataframe(data)
    new_results, last_year = predict(df, steps)
    new_years = [datetime.datetime(year=year,month=1,day=1) for year in range(last_year,last_year+steps)]
    for index,val in enumerate(new_years) :
        s = pd.Series()
        s = s.set_value("cpi", new_results[index])
        s.name = val
        df = df.append(s)
    df.sort_index(inplace=True)
    return df.to_dict()

#http://stackoverflow.com/questions/13331518/how-to-add-a-single-item-to-a-pandas-series
#http://stackoverflow.com/questions/16824607/pandas-appending-a-row-to-a-dataframe-and-specify-its-index-label
