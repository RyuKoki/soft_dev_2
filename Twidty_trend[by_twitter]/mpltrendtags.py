from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

import matplotlib.pyplot as plt
    
class MplTrendtags(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(plt.figure(figsize=(4, 3)))
        plt.rcParams['font.family'] = 'Sarabun'
        plt.rcParams['font.size'] = 8
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.subplots()
        self.canvas.axes.get_xticklabels(15)
        self.setLayout(vertical_layout)