from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Twidty import Twidty
from NewsCrawler import NewsCrawler
import datetime, functools, operator, collections

class SearchDBProgress(QDialog):
	def __init__(self, twitter_key, crawler_key, start, stop):
		super().__init__()
		self.twitter_key = twitter_key
		self.crawler_key = crawler_key
		self.start = start
		self.stop = stop

		self.setWindowTitle("Search in Process")

		self.lable_text = QLabel("Searching in database ...")

		self.progress_bar = QProgressBar()
		self.progress_bar.setStyle(QStyleFactory.create("Windows"))
		self.progress_bar.setTextVisible(True)

		self.analyze_btn = QPushButton("Start analyzing")
		self.analyze_btn.setEnabled(True)
		self.analyze_btn.setDefault(True)
		self.analyze_btn.clicked.connect(self.evt_analyz_btn)

		self.finish_btn = QPushButton("Show up analyzing")
		self.finish_btn.setEnabled(False)

		self.btn_layout = QHBoxLayout()
		self.btn_layout.addWidget(self.analyze_btn)
		self.btn_layout.addWidget(self.finish_btn)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.lable_text)
		self.layout.addWidget(self.progress_bar)
		self.layout.addLayout(self.btn_layout)
		self.setLayout(self.layout)

	def evt_analyz_btn(self):
		self.analyze_btn.setEnabled(False)
		self.worker = SearchDBThread(self, self.twitter_key, self.crawler_key, self.start, self.stop)
		self.worker.start()
		self.worker.update_progress.connect(self.evt_update_progress)
		self.worker.finished.connect(self.evt_finish_btn)

	def evt_update_progress(self, vals):
		self.progress_bar.setValue(vals)

	def evt_finish_btn(self):
		print("=====twitter=====")
		print(self.worker.twitter_freq_result)
		print(self.worker.twitter_sent_result)
		print("=====crawler=====")
		print(self.worker.crawler_freq_result)
		print(self.worker.crawler_sent_result)
		self.finish_btn.setEnabled(True)
		self.finish_btn.clicked.connect(self.close)
		return True

	def analyze_result(self):
		return {
			"twitter_results":{
			"related_words":self.worker.twitter_freq_result, 
			"sentiment":self.worker.twitter_sent_result
			}, 
			"crawler_results":{ 
			"related_words":self.worker.crawler_freq_result, 
			"sentiment":self.worker.crawler_sent_result
			}
		}


class SearchDBThread(QThread):
	update_progress = pyqtSignal(int)

	def __init__(self, parent=None, twitter_key="", crawler_key="", start="", stop=""):
		super(QThread, self).__init__(parent)
		self.twitter_key = twitter_key
		self.crawler_key = crawler_key
		self.start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
		self.stop_date = datetime.datetime.strptime(stop, "%Y-%m-%d")
		self.delta_date = self.stop_date - self.start_date
		self.step_date = datetime.timedelta(days=1)
		self.twidty = Twidty()
		self.crawler = NewsCrawler()

		self.twitter_freq_result = None
		self.twitter_sent_result = None
		self.crawler_freq_result = None
		self.crawler_sent_result = None

	def run(self):
		counter_progress = 0
		twitter_freq = []
		twitter_sent = []
		crawler_freq = []
		crawler_sent = []
		if self.delta_date.days == 0:
			delta_day = 1
		else:
			delta_day = self.delta_date.days + 1
		percentage = int(round(((1 / delta_day) * 100), 0))
		# separate_percent = int(round(percentage / 2, 0))
		while self.start_date <= self.stop_date:
			print("Search in ... ", str(self.start_date.date()))
			# counter_progress += separate_percent
			# self.update_progress.emit(counter_progress)
			on_twitter = self.twidty.search(	self.twitter_key, 
											str(self.start_date.date()), 
											str(self.start_date.date())		)
			twitter_freq.append(on_twitter["related_words"])
			twitter_sent.append(on_twitter["sentiment"])

			on_crawler = self.crawler.search(	self.crawler_key, 
											str(self.start_date.date()), 
											str(self.start_date.date())		)
			crawler_freq.append(on_crawler["related_words"])
			crawler_sent.append(on_crawler["sentiment"])
			counter_progress += percentage
			self.update_progress.emit(counter_progress)
			self.start_date += self.step_date
		
		twitter_freq_sum = self.twidty.merge_many_ranking(self.twitter_key, twitter_freq)
		twitter_sent_sum = self.twidty.merge_many_ranking(self.twitter_key, twitter_sent)
		crawler_freq_sum = self.twidty.merge_many_ranking(self.crawler_key, crawler_freq)
		crawler_sent_sum = self.twidty.merge_many_ranking(self.crawler_key, crawler_sent)

		self.twitter_freq_result = dict(sorted(twitter_freq_sum.items(), 
										key=operator.itemgetter(1), 
										reverse=True)[:5])
		self.twitter_sent_result = dict(sorted(twitter_sent_sum.items(), 
										key=operator.itemgetter(1), 
										reverse=True)[:5])
		self.crawler_freq_result = dict(sorted(crawler_freq_sum.items(), 
										key=operator.itemgetter(1), 
										reverse=True)[:5])
		self.crawler_sent_result = dict(sorted(crawler_sent_sum.items(), 
										key=operator.itemgetter(1), 
										reverse=True)[:5])

	

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	test = SearchDBProgress(twitter_key='intuch', crawler_key='intuch', start="2021-04-21", stop="2021-04-21")
	test.show()
	sys.exit(app.exec_())
