from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys, datetime, os, operator
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
		# set progressbar on twitter and crawler
		self.news_prg_bar.setVisible(False)
		self.twitter_prg_bar.setVisible(False)
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
		self.search_btn.clicked.connect(self.twitter_search)
		self.search_btn.clicked.connect(self.crawler_search)
		self.submit_btn.clicked.connect(self.search_stock)
		########################################
		self.trendy()
		########################################
		# init function from another files
		self.twidty = Twidty()
		self.crawler = NewsCrawler()

	def crawler_search(self):
		crawler_key = self.news_input.text()
		if crawler_key == "":
			# self.news_related_widget.canvas.clear(True)
			# self.news_sentiment_widget.canvas.clear(True)
			self.news_related_widget.setStyleSheet('background-color: rgb(255, 255, 255);')
			self.news_sentiment_widget.setStyleSheet('background-color: rgb(255, 255, 255);')
		else:
			start_date = self.start_date.text()
			stop_date = self.stop_date.text()
			self.news_prg_bar.setVisible(True)
			self.crawler_worker = CrawlerThread(self, crawler_key, start_date, stop_date)
			self.crawler_worker.start()
			self.crawler_worker.update_prg.connect(self.evt_crawler_prg)
			self.crawler_worker.finished.connect(self.evt_crawler_finish)

	def evt_crawler_prg(self, vals):
		self.news_prg_bar.setValue(vals)

	def evt_crawler_finish(self):
		self.news_prg_bar.setVisible(False)
		crawler_result = {
							"related_words":self.crawler_worker.crawler_freq_result, 
							"sentiment":self.crawler_worker.crawler_sent_result
						}
		self.crawler_plot(crawler_result)

	def twitter_search(self):
		twitter_key = self.twitter_input.text()
		if twitter_key == "":
			# self.twitter_related_widget.canvas.clear(True)
			# self.twitter_sentiment_widget.canvas.clear(True)
			self.twitter_related_widget.setStyleSheet('background-color: rgb(255, 255, 255);')
			self.twitter_sentiment_widget.setStyleSheet('background-color: rgb(255, 255, 255);')
		else:
			start_date = self.start_date.text()
			stop_date = self.stop_date.text()
			twitter_result = self.twidty.search(twitter_key, start_date, stop_date)
			if twitter_result == False:
				user_response = self.twitter_alert_search()
				if user_response == QMessageBox.Ok:
					self.PopUp = NewSearchProgress(twitter_key, start_date, stop_date)
					self.PopUp.exec()
			elif twitter_result == True:
				user_response = self.twitter_alert_update()
				if user_response == QMessageBox.Ok:
					self.PopUp = NewSearchProgress(twitter_key, start_date, stop_date)
					self.PopUp.exec()
			print('start analyze')
			self.twitter_prg_bar.setVisible(True)
			self.twitter_worker = TwitterThread(self, twitter_key, start_date, stop_date)
			self.twitter_worker.start()
			self.twitter_worker.update_prg.connect(self.evt_twitter_prg)
			self.twitter_worker.finished.connect(self.evt_twitter_finish)
		
	def evt_twitter_prg(self, vals):
		self.twitter_prg_bar.setValue(vals)

	def evt_twitter_finish(self):
		self.twitter_prg_bar.setVisible(False)
		twitter_result = {
							"related_words":self.twitter_worker.twitter_freq_result, 
							"sentiment":self.twitter_worker.twitter_sent_result
						}
		self.twitter_plot(twitter_result)

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

	def search_stock(self):
		print('stock')
		self.stock()

class TwitterThread(QThread):

	update_prg = pyqtSignal(int)

	def __init__(self, parent=None, keyword="", start="", stop=""):
		super(QThread, self).__init__(parent)
		self.keyword = keyword
		self.start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
		self.stop_date = datetime.datetime.strptime(stop, "%Y-%m-%d")
		self.time_delta = self.stop_date - self.start_date
		self.step = datetime.timedelta(days=1)
		self.twidty = Twidty()
		self.twitter_freq_result = None
		self.twitter_sent_result = None

	def run(self):
		counter_prg = 0
		twitter_freq = []
		twitter_sent = []
		if self.time_delta.days == 0:
			delta_day = 1
		else:
			delta_day = self.time_delta.days + 1
		percentage = int(round((1/delta_day)*100, 0))
		while self.start_date <= self.stop_date:
			print("twitter search in ... ", str(self.start_date.date()))
			on_twitter = self.twidty.search(self.keyword, 
											str(self.start_date.date()), 
											str(self.start_date.date()))
			twitter_freq.append(on_twitter['related_words'])
			twitter_sent.append(on_twitter['sentiment'])
			counter_prg += percentage
			self.update_prg.emit(counter_prg)
			self.start_date += self.step

		twitter_freq_sum = self.twidty.merge_many_ranking(self.keyword, twitter_freq)
		twitter_sent_sum = self.twidty.merge_many_ranking(self.keyword, twitter_sent)

		self.twitter_freq_result = dict(sorted(twitter_freq_sum.items(), 
										key=operator.itemgetter(1), 
										reverse=True)[:5])
		self.twitter_sent_result = dict(sorted(twitter_sent_sum.items(), 
										key=operator.itemgetter(1), 
										reverse=True)[:5])

class CrawlerThread(QThread):

	update_prg = pyqtSignal(int)

	def __init__(self, parent=None, keyword="", start="", stop=""):
		super(QThread, self).__init__(parent)
		self.keyword = keyword
		self.start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
		self.stop_date = datetime.datetime.strptime(stop, "%Y-%m-%d")
		self.time_delta = self.stop_date - self.start_date
		self.step = datetime.timedelta(days=1)
		self.twidty = Twidty()
		self.crawler = NewsCrawler()
		self.crawler_freq_result = None
		self.crawler_sent_result = None

	def run(self):
		counter_prg = 0
		crawler_freq = []
		crawler_sent = []
		if self.time_delta.days == 0:
			delta_day = 1
		else:
			delta_day = self.time_delta.days + 1
		percentage = int(round((1/delta_day)*100, 0))
		while self.start_date <= self.stop_date:
			print("crawler search in ... ", str(self.start_date.date()))
			on_crawler = self.crawler.search(self.keyword, 
											str(self.start_date.date()), 
											str(self.start_date.date()))
			crawler_freq.append(on_crawler['related_words'])
			crawler_sent.append(on_crawler['sentiment'])
			counter_prg += percentage
			self.update_prg.emit(counter_prg)
			self.start_date += self.step

		crawler_freq_sum = self.twidty.merge_many_ranking(self.keyword, crawler_freq)
		crawler_sent_sum = self.twidty.merge_many_ranking(self.keyword, crawler_sent)

		self.crawler_freq_result = dict(sorted(crawler_freq_sum.items(), 
										key=operator.itemgetter(1), 
										reverse=True)[:5])
		self.crawler_sent_result = dict(sorted(crawler_sent_sum.items(), 
										key=operator.itemgetter(1), 
										reverse=True)[:5])

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Ui_MainWindow()
	window.show()
	app.exec_()

