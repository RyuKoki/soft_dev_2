from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys, datetime, threading

from mpl_related_news import mpl_related_news
from mpl_related_twitter import mpl_related_twitter
from mpl_sentiment_news import mpl_sentiment_news
from mpl_sentiment_twitter import mpl_sentiment_twitter
from mpl_stock import mpl_stock

from Twidty import Twidty
from NewsCrawler import NewsCrawler
from Stock import Stock

from TwitterThread import TwitterThread


class Ui_MainWindow(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)
		loadUi("GUI_MainWindow.ui", self)
		########################################
		today_time = datetime.datetime.now()
		today_date = today_time.date()
		self.start_date.setDate(today_date)
		self.start_date.setMaximumDate(today_date)
		self.stop_date.setDate(today_date)
		self.stop_date.setMaximumDate(today_date)
		########################################
		self.search_btn.clicked.connect(self.search_analysis)
		self.submit_btn.clicked.connect(self.search_stock)
		########################################

	def twitter(self):
		twidty = Twidty()
		keyword = self.twitter_input.text()
		if keyword == "":
			self.twitter_related_widget.canvas.axes.clear()
			self.twitter_sentiment_widget.canvas.axes.clear()
		else:
			start_date = self.start_date.text()
			stop_date = self.stop_date.text()
			get_result = twidty.search(keyword, start_date, stop_date)
			if get_result == False:
				response = self.twitter_alert_search()
				if response == QMessageBox.Ok:
					print("search now")
			elif type(get_result) == list:
				response = self.twitter_alert_update()
				if response == QMessageBox.Ok:
					print("update now")
					update_thr = threading.Thread(target=twidty.search_data_by_date, args=(keyword, start_date, ))
					update_thr.start()
			else:
				print('show data')
				#############related words##############
				related = get_result['related_words']
				words_lb = list(related.keys())
				words_sz = related.values()
				self.twitter_related_widget.canvas.axes.clear()
				self.twitter_related_widget.canvas.axes.bar(words_lb, words_sz)
				self.twitter_related_widget.canvas.axes.tick_params(axis='x', rotation=15)
				self.twitter_related_widget.canvas.draw()
				#############sentiment##############
				sentiment = get_result['sentiment']
				sent_lb = list(sentiment.keys())
				sent_sz = sentiment.values()
				self.twitter_sentiment_widget.canvas.axes.clear()
				self.twitter_sentiment_widget.canvas.axes.pie(sent_sz, 
																labels=sent_lb, 
																autopct='%1.1f%%', 
																startangle=10)
				self.twitter_sentiment_widget.canvas.draw()

	def twitter_alert_search(self):
		alert = QMessageBox()
		alert.setWindowTitle("Search Alert")
		alert.setIcon(QMessageBox.Warning)
		alert.setText("This is a new keyword! \n Would you mind if wait several minutes!")
		# alert.setInformativeText("")
		alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		response = alert.exec()
		# print(response)
		return response

	def twitter_alert_update(self):
		alert = QMessageBox()
		alert.setWindowTitle("Update Alert")
		alert.setIcon(QMessageBox.Warning)
		alert.setText("Please update!")
		alert.setStandardButtons(QMessageBox.Ok)
		response = alert.exec()
		return response

	def search_analysis(self):
		print('search')
		self.twitter()

	def search_stock(self):
		print('stock')


if __name__ == "__main__":
	app = QApplication([])
	window = Ui_MainWindow()
	window.show()
	app.exec_()
