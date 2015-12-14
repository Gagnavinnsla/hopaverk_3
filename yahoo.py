from pandas_datareader import data as web
import pandas as pd
import numpy as np
import datetime
from datetime import date

start = datetime.datetime(2010,1,1)
today = datetime.datetime.today()
end = today

x = web.DataReader(ticker,'yahoo',start,end)

