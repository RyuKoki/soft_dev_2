# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Twidty_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from mplpoptrend import MplPoptrend
from mpltrendtags import MplTrendtags
from Twidty_backend import Twidty
from keyword_alert import Ui_Dialog as keyword_dialog
from search_alert import Ui_Dialog as search_dialog
from search_process import Ui_Dialog as search_p_dialog
import datetime, threading


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 675)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 675))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 675))
        font = QtGui.QFont()
        font.setFamily("CS PraKas")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.keyword_input = QtWidgets.QLineEdit(self.centralwidget)
        self.keyword_input.setGeometry(QtCore.QRect(20, 20, 560, 70))
        font = QtGui.QFont()
        font.setFamily("Sarabun")
        font.setPointSize(20)
        self.keyword_input.setFont(font)
        self.keyword_input.setObjectName("keyword_input")
        self.separate_line = QtWidgets.QFrame(self.centralwidget)
        self.separate_line.setGeometry(QtCore.QRect(580, 0, 40, 675))
        self.separate_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.separate_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.separate_line.setObjectName("separate_line")
        self.label_date = QtWidgets.QLabel(self.centralwidget)
        self.label_date.setGeometry(QtCore.QRect(20, 90, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Sarabun")
        font.setPointSize(20)
        self.label_date.setFont(font)
        self.label_date.setObjectName("label_date")
        self.date_start = QtWidgets.QDateEdit(self.centralwidget)
        self.date_start.setGeometry(QtCore.QRect(120, 100, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Sarabun")
        font.setPointSize(14)
        date = datetime.datetime.now()
        self.date_start.setFont(font)
        self.date_start.setCalendarPopup(True)
        self.date_start.setTimeSpec(QtCore.Qt.LocalTime)
        self.date_start.setDate(date.date())
        self.date_start.setMinimumDate(datetime.date(2021, 2, 1))
        self.date_start.setMaximumDate(date.date())
        self.date_start.setObjectName("date_start")
        self.label_line = QtWidgets.QLabel(self.centralwidget)
        self.label_line.setGeometry(QtCore.QRect(250, 90, 20, 50))
        font = QtGui.QFont()
        font.setFamily("Sarabun")
        font.setPointSize(20)
        self.label_line.setFont(font)
        self.label_line.setObjectName("label_line")
        self.date_stop = QtWidgets.QDateEdit(self.centralwidget)
        self.date_stop.setGeometry(QtCore.QRect(270, 100, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Sarabun")
        font.setPointSize(14)
        self.date_stop.setFont(font)
        self.date_stop.setCalendarPopup(True)
        self.date_stop.setTimeSpec(QtCore.Qt.LocalTime)
        self.date_stop.setDate(date.date())
        self.date_stop.setMinimumDate(datetime.date(2021, 2, 1))
        self.date_stop.setMaximumDate(date.date())
        self.date_stop.setObjectName("date_stop")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(400, 100, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Sarabun")
        font.setPointSize(14)
        self.search_button.setFont(font)
        self.search_button.setObjectName("search_button")
        self.label_poptrend = QtWidgets.QLabel(self.centralwidget)
        self.label_poptrend.setGeometry(QtCore.QRect(20, 140, 560, 30))
        font = QtGui.QFont()
        font.setFamily("Sarabun")
        font.setPointSize(18)
        self.label_poptrend.setFont(font)
        self.label_poptrend.setObjectName("label_poptrend")
        self.poptrend_line = QtWidgets.QFrame(self.centralwidget)
        self.poptrend_line.setGeometry(QtCore.QRect(20, 160, 560, 40))
        self.poptrend_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.poptrend_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.poptrend_line.setObjectName("poptrend_line")
        self.widget_showgraph = MplPoptrend(self.centralwidget)
        self.widget_showgraph.setGeometry(QtCore.QRect(19, 190, 560, 440))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_showgraph.sizePolicy().hasHeightForWidth())
        self.widget_showgraph.setSizePolicy(sizePolicy)
        self.widget_showgraph.setMinimumSize(QtCore.QSize(560, 440))
        self.widget_showgraph.setMaximumSize(QtCore.QSize(560, 440))
        self.widget_showgraph.setObjectName("widget_showgraph")
        self.label_trendtags = QtWidgets.QLabel(self.centralwidget)
        self.label_trendtags.setGeometry(QtCore.QRect(620, 20, 560, 30))
        font = QtGui.QFont()
        font.setFamily("Sarabun")
        font.setPointSize(18)
        self.label_trendtags.setFont(font)
        self.label_trendtags.setObjectName("label_trendtags")
        self.trendtags_line = QtWidgets.QFrame(self.centralwidget)
        self.trendtags_line.setGeometry(QtCore.QRect(620, 40, 560, 40))
        self.trendtags_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.trendtags_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.trendtags_line.setObjectName("trendtags_line")
        self.widget_showtrend = MplTrendtags(self.centralwidget)
        self.widget_showtrend.setGeometry(QtCore.QRect(620, 280, 560, 350))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_showtrend.sizePolicy().hasHeightForWidth())
        self.widget_showtrend.setSizePolicy(sizePolicy)
        self.widget_showtrend.setMinimumSize(QtCore.QSize(560, 350))
        self.widget_showtrend.setMaximumSize(QtCore.QSize(560, 350))
        self.widget_showtrend.setObjectName("widget_showtrend")
        self.widget_showtrendtags = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.widget_showtrendtags.setGeometry(QtCore.QRect(620, 70, 560, 200))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_showtrendtags.sizePolicy().hasHeightForWidth())
        self.widget_showtrendtags.setSizePolicy(sizePolicy)
        self.widget_showtrendtags.setMinimumSize(QtCore.QSize(560, 200))
        self.widget_showtrendtags.setMaximumSize(QtCore.QSize(560, 200))
        font = QtGui.QFont()
        font.setFamily("Sarabun")
        font.setPointSize(16)
        self.widget_showtrendtags.setFont(font)
        self.widget_showtrendtags.setReadOnly(True)
        self.widget_showtrendtags.setObjectName("widget_showtrendtags")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.search_button.clicked.connect(self.poptrend_graph)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Twidty"))
        self.label_date.setText(_translate("MainWindow", "DATE :: "))
        self.date_start.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.label_line.setText(_translate("MainWindow", "-"))
        self.date_stop.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.search_button.setText(_translate("MainWindow", "SEARCH"))
        self.label_poptrend.setText(_translate("MainWindow", "Popularity Trend"))
        self.label_trendtags.setText(_translate("MainWindow", "Trendy Hashtags"))
        self.trendtags_graph()
        self.show_trendtags()

    def poptrend_graph(self):
        # print('poptrend')
        keyword = self.keyword_input.text()
        if keyword != "":
            twidty = Twidty()
            dict_result = twidty.frequency_analysis(keyword, self.date_start.text(), self.date_stop.text())
            if dict_result != False:
                name = dict_result.keys()
                size = dict_result.values()

                self.widget_showgraph.canvas.axes.clear()
                self.widget_showgraph.canvas.axes.set_title(keyword)
                self.widget_showgraph.canvas.axes.pie(size, labels=name, 
                                                            autopct='%1.1f%%',  
                                                            startangle=10, )

                self.widget_showgraph.canvas.draw()
                self.keyword_input.setText("")
                date = datetime.datetime.now()
                self.date_start.setDate(date.date())
                self.date_stop.setDate(date.date())
            else:
                Dialog = QtWidgets.QDialog()
                ui = search_dialog()
                ui.setupUi(Dialog)
                Dialog.show()
                user_acting = Dialog.exec_()
                if user_acting == QtWidgets.QDialog.Accepted:
                    # twidty.search(keyword)
                    thr_search = threading.Thread(target=twidty.search, args=(keyword, ))
                    thr_search.start()
                    if thr_search.is_alive():
                        s_Dialog = QtWidgets.QDialog()
                        s_ui = search_p_dialog()
                        s_ui.setupUi(s_Dialog)
                        s_Dialog.show()
                        thr_search.join()
                        s_Dialog.exec_()

                    self.keyword_input.setText("")
                    date = datetime.datetime.now()
                    self.date_start.setDate(date.date())
                    self.date_stop.setDate(date.date())

        else:
            Dialog = QtWidgets.QDialog()
            ui = keyword_dialog()
            ui.setupUi(Dialog)
            Dialog.show()
            Dialog.exec_()

    def trendtags_graph(self):
        # print('trendtags')
        twidty = Twidty()
        trendy_now = twidty.trend_tags(5)
        labels = list(trendy_now.keys())
        sizes = list(trendy_now.values())
        self.widget_showtrend.canvas.axes.clear()
        self.widget_showtrend.canvas.axes.bar(labels, sizes, 
                        color=['red', 'green', 'blue', 'orange', 'pink'])
        self.widget_showtrend.canvas.axes.tick_params(axis='x', rotation=10)
        self.widget_showtrend.canvas.draw()

    def show_trendtags(self):
        twidty = Twidty()
        trend_now = twidty.trend_tags(10)
        name = list(trend_now.keys())
        for number in range(len(trend_now)):
            text = "{}\t{}".format(number+1, name[number])
            self.widget_showtrendtags.appendPlainText(text)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
