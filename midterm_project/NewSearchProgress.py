from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os, datetime
from Twidty import Twidty

class NewSearchProgress(QDialog):
	def __init__(self, keyword, start, stop):
		super().__init__()
		self.keyword = keyword
		self.start_d = start
		self.stop_d = stop

		self.setWindowTitle("Keyword Search Alert")

		self.progress_bar = QProgressBar()
		self.progress_bar.setStyle(QStyleFactory.create("Windows"))
		self.progress_bar.setTextVisible(True)

		self.search_now_btn = QPushButton("Search Now")
		self.search_now_btn.setDefault(True)
		self.search_now_btn.clicked.connect(self.evt_start_btn)

		self.finish_btn = QPushButton("Finish")
		self.finish_btn.setEnabled(False)

		self.cancel_btn = QPushButton("Cancel")
		self.cancel_btn.clicked.connect(self.close)

		self.layout_btn = QHBoxLayout()
		self.layout_btn.addWidget(self.search_now_btn)
		self.layout_btn.addWidget(self.finish_btn)
		self.layout_btn.addWidget(self.cancel_btn)

		self.lable_text = QLabel("Searching in process ...")

		self.layout_main = QVBoxLayout()
		self.layout_main.addWidget(self.lable_text)
		self.layout_main.addWidget(self.progress_bar)
		self.layout_main.addLayout(self.layout_btn)
		self.setLayout(self.layout_main)

	def evt_start_btn(self):
		self.search_now_btn.setEnabled(False)
		self.worker = NewSearchThread(self, self.keyword, self.start_d, self.stop_d)
		self.worker.start()
		self.worker.update_progress.connect(self.evt_update_progress)
		self.worker.finished.connect(self.evt_finish_btn)
		
	def evt_update_progress(self, vals):
		self.progress_bar.setValue(vals)

	def evt_finish_btn(self):
		self.finish_btn.setEnabled(True)
		self.finish_btn.clicked.connect(self.close)
		return True

class NewSearchThread(QThread):
	update_progress = pyqtSignal(int)
	def __init__(self, parent=None, keyword="", start="", stop=""):
		super(QThread, self).__init__(parent)
		self.keyword = keyword
		self.start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
		self.stop_date = datetime.datetime.strptime(stop, "%Y-%m-%d")
		self.delta_date = self.stop_date - self.start_date
		self.step_date = datetime.timedelta(days=1)
		self.twidty = Twidty()
		self.old_data = os.listdir(self.twidty.save_file_path + r"\{}".format(self.keyword))

	def run(self):
		counter_progress = 0
		if self.delta_date.days == 0:
			delta_day = 1
		else:
			delta_day = self.delta_date.days + 1
		percentage = (1 / delta_day) * 100
		while self.start_date <= self.stop_date:
			if str(self.start_date.date())+".csv" not in self.old_data:
				print("Searching...")
				counter_progress += int(round(percentage/2, 0))
				self.update_progress.emit(counter_progress)
				self.twidty.save_new_data(self.keyword, str(self.start_date.date()))
				counter_progress += int(round(percentage/2, 0))
				self.update_progress.emit(counter_progress)
				self.start_date += self.step_date
			else:
				counter_progress += int(round(percentage, 0))
				self.update_progress.emit(counter_progress)
				self.start_date += self.step_date
