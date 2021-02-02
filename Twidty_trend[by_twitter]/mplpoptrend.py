from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

import matplotlib.pyplot as plt

    
class MplPoptrend(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(plt.figure())
        plt.rcParams['font.family'] = 'Sarabun'
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.subplots()
        self.canvas.axes.get_xaxis().set_visible(False)
        self.canvas.axes.get_yaxis().set_visible(False)
        self.setLayout(vertical_layout)