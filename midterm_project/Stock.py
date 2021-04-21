import pandas_datareader as pdr
import datetime

class Stock(object):

	def get_stock(self, stock_name, start, end):
		# convert start and end date from string to datetime
		start_d = datetime.datetime.strptime(start, '%Y-%m-%d')
		end_d = datetime.datetime.strptime(end, '%Y-%m-%d')
		# get data of stock
		df = pdr.get_data_yahoo(stock_name, start_d, end_d)
		# keep data which we want price
		df = df[['Open', 'High', 'Low', 'Close']]
		return df

# stock = Stock()
# result = stock.get_stock('PTT.BK', '2021-03-01', '2021-03-17')
# print(result)