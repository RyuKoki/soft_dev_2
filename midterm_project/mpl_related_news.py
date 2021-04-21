from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas 
import matplotlib.pyplot as plt

class mpl_related_news(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.canvas = FigureCanvas(plt.figure())
		plt.rcParams['font.family'] = 'Leelawadee'
		plt.rcParams['font.size'] = 20
		vertical_layout = QVBoxLayout()
		vertical_layout.addWidget(self.canvas)
		self.canvas.axes = self.canvas.figure.add_subplot(111)
		self.canvas.figure.subplots_adjust(bottom=0.5)
		self.canvas.axes.axis("off")
		self.setLayout(vertical_layout)