import pandas.io.data as web
from web import Options

aapl = Options('AAPL')
puts, calls = appl.get_options_data()