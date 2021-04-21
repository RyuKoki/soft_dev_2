from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys, datetime, os
from PyQt5 import QtGui

from mpl_related_news import mpl_related_news
from mpl_related_twitter import mpl_related_twitter
from mpl_sentiment_news import mpl_sentiment_news
from mpl_sentiment_twitter import mpl_sentiment_twitter
from mpl_stock import mpl_stock

from Twidty import Twidty
from NewsCrawler import NewsCrawler
from Stock import Stock

from NewSearchProgress import NewSearchProgress
from SearchDBProgress import SearchDBProgress

import matplotlib.dates as mpldates
from mplfinance.original_flavor import candlestick_ohlc


class Ui_MainWindow(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)
		# loading GUI that design in QtDesigner by .ui type file
		loadUi("GUI_MainWindow.ui", self)
		########################################
		# set maximum date for choosing by today
		today_time = datetime.datetime.now()
		today_date = today_time.date()
		self.start_date.setDate(today_date)
		self.start_date.setMaximumDate(today_date)
		self.stop_date.setDate(today_date)
		self.stop_date.setMaximumDate(today_date)
		########################################
		# connect all push button functions
		self.search_btn.clicked.connect(self.show_up_analyze)
		self.submit_btn.clicked.connect(self.search_stock)
		########################################
		self.trendy()
		########################################
		# init function from another files
		self.twidty = Twidty()
		self.crawler = NewsCrawler()

	def main_search(self):
		twidty = Twidty()
		news_crawler = NewsCrawler()
		keyword = self.twitter_input.text()
		if keyword == "":
			self.twitter_related_widget.canvas.axes.clear()
			self.twitter_related_widget.canvas.axes.axis("off")
			self.twitter_sentiment_widget.canvas.axes.clear()
		else:
			start_date = self.start_date.text()
			stop_date = self.stop_date.text()
			twitter_get_result = twidty.search(keyword, start_date, stop_date)
			if twitter_get_result == False:
				print('new keyword')
				user_response = self.twitter_alert_search()
				if user_response == QMessageBox.Ok:
					print("Okay search now")
					self.PopUp = NewSearchProgress(keyword, start_date, stop_date)
					self.PopUp.exec()
			elif twitter_get_result == True:
				print('update keyword')
				user_response = self.twitter_alert_update()
				if user_response == QMessageBox.Ok:
					print("Okay update now")
					self.PopUp = NewSearchProgress(keyword, start_date, stop_date)
					self.PopUp.exec()
			print('searching...')
			self.search_prg = SearchDBProgress(keyword, start_date, stop_date)
			self.search_prg.exec()
			if self.search_prg.evt_finish_btn() == True:
				print("SUCCESS!")
				all_results = self.search_prg.analyze_result()
				self.twitter_plot(all_results['twitter_results'])
				self.crawler_plot(all_results['crawler_results'])

	def twitter_search(self):
		twitter_key = self.twitter_input.text()
		crawler_key = self.news_input.text()
		if twitter_key == "":
			self.twitter_related_widget.canvas.clear(True)
			self.twitter_sentiment_widget.canvas.clear(True)
		elif crawler_key == "":
			self.news_related_widget.canvas.clear(True)
			self.news_sentiment_widget.canvas.clear(True)
		else:
			start_date = self.start_date.text()
			stop_date = self.stop_date.text()
			twitter_result = self.twidty.search(twitter_key, start_date, stop_date)
			if twitter_result == False:
				user_alert = self.twitter_alert_search()
				if user_alert == QMessageBox.Ok:
					self.new_search_prg = NewSearchProgress(twitter_key, start_date, stop_date)
					self.new_search_prg.exec()
			elif twitter_result == True:
				user_alert = self.twitter_alert_update()
				if user_alert == QMessageBox.Ok:
					self.search_db = NewSearchProgress(twitter_key, start_date, stop_date)
					self.search_db.exec()
			self.progress_search = SearchDBProgress(keyword, start, stop)

	def twitter_plot(self, dict_data):
		#############related words##############
		related = dict_data['related_words']
		words_lb = list(related.keys())
		words_sz = related.values()
		self.twitter_related_widget.canvas.axes.clear()
		self.twitter_related_widget.canvas.axes.bar(words_lb, words_sz)
		self.twitter_related_widget.canvas.axes.tick_params(axis='x', rotation=15)
		self.twitter_related_widget.canvas.draw()
		#############sentiment##############
		sentiment = dict_data['sentiment']
		sent_lb = list(sentiment.keys())
		sent_sz = sentiment.values()
		self.twitter_sentiment_widget.canvas.axes.clear()
		self.twitter_sentiment_widget.canvas.axes.pie(sent_sz, 
													labels=sent_lb, 
													autopct='%1.1f%%', 
													startangle=10)
		self.twitter_sentiment_widget.canvas.draw()

	def crawler_plot(self, dict_data):
		##############mostly web post keyword############
		related = dict_data['related_words']
		web_lb = list(related.keys())
		web_sz = related.values()
		if sum(list(web_sz)) == 0:
			self.news_related_widget.canvas.axes.clear()
		else:
			self.news_related_widget.canvas.axes.clear()
			self.news_related_widget.canvas.axes.bar(web_lb, web_sz)
			self.news_related_widget.canvas.axes.tick_params(axis='x', rotation=90)
			self.news_related_widget.canvas.draw()
		############sentiment#############
		sentiment = dict_data['sentiment']
		sent_lb = sentiment.keys()
		sent_sz = sentiment.values()
		if sum(list(sent_sz)) == 0:
			self.news_sentiment_widget.canvas.axes.clear()
		else:
			self.news_sentiment_widget.canvas.axes.clear()
			self.news_sentiment_widget.canvas.axes.pie(sent_sz, 
													labels=sent_lb, 
													autopct='%1.1f%%', 
													startangle=10, )
			self.news_sentiment_widget.canvas.draw()

	def trendy(self):
		twidty = Twidty()
		intrend = twidty.trendy()
		model = QtGui.QStandardItemModel()
		self.listView.setModel(model)
		for tren in intrend:
			item = QtGui.QStandardItem(tren)
			model.appendRow(item)

	def stock(self):
		stock = Stock()
		stock_symbol = self.stock_input.text()
		if stock_symbol == "":
			self.stock_widget.canvas.axes.clear()
		else:
			start_date = self.start_date.text()
			stop_date = self.stop_date.text()
			stock_data = stock.get_stock(stock_symbol, start_date, stop_date)
			stock_data.reset_index(inplace=True)
			stock_data['Date'] = stock_data['Date'].map(mpldates.date2num)
			self.stock_widget.canvas.axes.clear()
			self.stock_widget.canvas.axes.grid(True)
			self.stock_widget.canvas.axes.set_ylabel("Price (Bath)")
			candlestick_ohlc(self.stock_widget.canvas.axes, 
							stock_data.values, 
							width=0.9, 
							colorup='green', colordown='red')
			self.stock_widget.canvas.axes.xaxis_date()
			self.stock_widget.canvas.axes.tick_params(axis='x', rotation=5)
			self.stock_widget.canvas.draw()

	def twitter_alert_search(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText("New Keyword! \n If you're OK, wait several minutes.")
		msg.setWindowTitle("New Keyword Alert")
		msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		reponse = msg.exec()
		return reponse

	def twitter_alert_update(self):
		alert = QMessageBox()
		alert.setWindowTitle("Update Alert")
		alert.setIcon(QMessageBox.Warning)
		alert.setText("This Keyword is updating now!")
		alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		response = alert.exec()
		return response

	def show_up_analyze(self):
		self.main_search()

	def search_stock(self):
		print('stock')
		self.stock()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Ui_MainWindow()
	window.show()
	app.exec_()
