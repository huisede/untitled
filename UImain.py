#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#  @Time     : 2017/12/6 11:15
#  @Author  :  LuChao
#  @Site     : 
#  @File     : UImain.py
#  @Software  : PyCharm


from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from test_ui import Ui_VI_Accessment_System
import sys
from Generate_Figs import *


class MainUiWindow(QMainWindow, Ui_VI_Accessment_System):

    def __init__(self, parent=None):
        super(MainUiWindow, self).__init__(parent)
        self.setupUi(self)
        self.menu_InputData.triggered.connect(self.load_sysgain_data)
        self.actionOveralwidget.triggered.connect(lambda: self.change_page(0))
        self.actionDataEdit.triggered.connect(lambda: self.change_page(1))
        self.actionRatingDetails.triggered.connect(lambda: self.change_page(2))
        self.treeWidget.clicked.connect(self.select_tree_nodes)
        self.pushButton_3.clicked.connect(self.button_clicked)  ###

    def change_page(self, index_page):
        self.stackedWidget.setCurrentIndex(index_page)

    def load_sysgain_data(self):
        filepath = QFileDialog.getOpenFileName(self, filter='*.csv')
        filepath_full = filepath[0]
        self.MainProcess_thread = ThreadProcess(method='sg_cal_thread', filepath=filepath_full)
        self.MainProcess_thread.Message_Finish.connect(self.show_ax_pictures)
        self.MainProcess_thread.start()

    def show_ax_pictures(self):

        dr = MyFigureCanvas(width=7, height=5, plot_type='3d',
                            data=self.MainProcess_thread.ax_holder_SG.accresponce.data,
                            para1=self.MainProcess_thread.ax_holder_SG.accresponce.pedal_avg)
        dr.plot_acc_response_()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(dr)
        self.PicToolBar = NavigationBar(dr, self)  # 初始化PicToolBar（本质为Wedgit），绑定到dr这个FigureCanvas上，然后将Toolbar绑到Layout上
        self.gridLayout_5.addWidget(self.PicToolBar)
        self.graphicsView_3.setScene(self.scene)
        self.graphicsView_3.show()

    def select_tree_nodes(self):
        a=self.treeWidget.currentItem().text(0)
        pass

    def add_combo_box(self):
        # button = QPushButton(u'测试', self)
        combo_box = QComboBox(self)
        self.verticalLayout_2.addWidget(combo_box)

    def button_clicked(self):
        self.MainProcess_thread = ThreadProcess(method='radar_cal_thread')
        self.MainProcess_thread.Message_Finish_2.connect(self.show_radar_pictures)
        self.MainProcess_thread.start()

    def show_radar_pictures(self, str):
        dr2 = MyFigureCanvas(width=10, height=5, plot_type='2d-poly',
                            data=self.MainProcess_thread.ax_holder_radar.theta,
                            para1=self.MainProcess_thread.ax_holder_radar.data)
        dr2.plot_radar_map_()
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(dr2)
        # self.PicToolBar = NavigationBar(dr, self)  # 初始化PicToolBar（本质为Wedgit），绑定到dr这个FigureCanvas上，然后将Toolbar绑到Layout上
        # self.gridLayout_5.addWidget(self.PicToolBar)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()


class ThreadProcess(QtCore.QThread):

    Message_Finish = QtCore.pyqtSignal(str)
    Message_Finish_2 = QtCore.pyqtSignal(str)

    def __init__(self, method, **kwargs):
        super(ThreadProcess, self).__init__()
        self.method = method
        self.kwargs = kwargs

    def run(self):
        try:
            getattr(self, self.method, 'nothing')()
        except BaseException as e:
            print(e)

    def sg_cal_thread(self):
        self.ax_holder_SG = sg_main(file_path=self.kwargs['filepath'])
        self.Message_Finish.emit("计算完成！")

    def radar_cal_thread(self):
        try:
            self.ax_holder_radar = radar_plot()
            self.Message_Finish_2.emit('finish')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ---------------QSS导入-------------------
    file = QtCore.QFile('css.qss')
    file.open(QtCore.QFile.ReadOnly)
    stylesheet = file.readAll()
    QtWidgets.QApplication.setStyleSheet(app, stylesheet.data().decode('utf-8'))  # utf-8  byte编码为String
    # ---------------实例化---------------------
    dlg = MainUiWindow()
    dlg.show()
    sys.exit(app.exec())
