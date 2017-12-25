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
from Generate_Figs import *
from Calculation_function import *
import sys


class MainUiWindow(QMainWindow, Ui_VI_Accessment_System):

    def __init__(self, parent=None):
        super(MainUiWindow, self).__init__(parent)
        self.setupUi(self)
        self.menu_InputData.triggered.connect(self.load_sysgain_data)
        self.actionOveralwidget.triggered.connect(lambda: self.change_main_page(0))
        self.actionDataEdit.triggered.connect(lambda: self.change_main_page(1))
        self.actionRatingDetails.triggered.connect(lambda: self.change_main_page(2))
        self.actionSettings.triggered.connect(lambda: self.change_main_page(3))
        self.actionComparison.triggered.connect(lambda: self.change_main_page(4))
        self.treeWidget.clicked.connect(self.select_tree_nodes)
        self.treeWidget_3.clicked.connect(self.select_tree3_nodes)
        self.pushButton_compare.clicked.connect(self.compare_radar_pic)
        self.pushButton_3.clicked.connect(self.button_clicked)  # test
        self.createContextMenu_RawDataView()

    # ---------------------------- 右键菜单 -----------------------------------------

    def createContextMenu_RawDataView(self):
        '''

        :return:
        '''
        self.graphicsView_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.graphicsView_2.customContextMenuRequested.connect(self.showContextMenu)
        self.graphicsView_2.contextMenu = QtWidgets.QMenu(self)
        self.graphicsView_2.actionA = self.graphicsView_2.contextMenu.addAction(QtGui.QIcon("images/0.png"), u'|  动作A')

        # 添加二级菜单
        self.graphicsView_2.second = self.graphicsView_2.contextMenu.addMenu(QtGui.QIcon("images/0.png"), u"|  二级菜单")
        self.graphicsView_2.actionD = self.graphicsView_2.second.addAction(QtGui.QIcon("images/0.png"), u'|  动作A')
        self.graphicsView_2.actionE = self.graphicsView_2.second.addAction(QtGui.QIcon("images/0.png"), u'|  动作B')
        self.graphicsView_2.actionF = self.graphicsView_2.second.addAction(QtGui.QIcon("images/0.png"), u'|  动作C')
        # 将动作与处理函数相关联
        # 这里为了简单，将所有action与同一个处理函数相关联，
        # 当然也可以将他们分别与不同函数关联，实现不同的功能
        return

    def showContextMenu(self, pos):
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        self.graphicsView_2.contextMenu.exec_(QtGui.QCursor.pos())  # 在鼠标位置显示
        # self.contextMenu.show()

    def change_main_page(self, index_page):
        self.stackedWidget.setCurrentIndex(index_page)

    def change_tree_stackedwidgets_page(self, stackedwidgets_id, index_page):
        eval('self.stackedWidget_' + str(stackedwidgets_id) + '.setCurrentIndex(index_page)')

    def load_sysgain_data(self):
        filepath = QFileDialog.getOpenFileName(self, filter='*.csv')
        filepath_full = filepath[0]
        self.MainProcess_thread = ThreadProcess(method='sg_cal_thread', filepath=filepath_full)
        self.MainProcess_thread.Message_Finish.connect(self.show_ax_pictures)
        self.MainProcess_thread.start()

    def show_ax_pictures(self):

        dr = MyFigureCanvas(width=7, height=5, plot_type='3d',
                            data=self.MainProcess_thread.ax_holder_SG.accresponce.data,
                            pedal_avg=self.MainProcess_thread.ax_holder_SG.accresponce.pedal_avg)
        dr.plot_acc_response_()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(dr)
        self.PicToolBar = NavigationBar(dr, self)  # 初始化PicToolBar（本质为Wedgit），绑定到dr这个FigureCanvas上，然后将Toolbar绑到Layout上
        self.gridLayout_5.addWidget(self.PicToolBar)
        self.graphicsView_3.setScene(self.scene)
        self.graphicsView_3.show()

    def show_data_edit_pictures(self, title):  # 原始数据编辑界面
        dr = MyFigureCanvas(width=16, height=8, plot_type='2d',
                            raw_data=self.MainProcess_thread.ax_holder_SG.rawdata,
                            title=title)
        dr.plot_raw_data()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(dr)
        self.PicToolBar = NavigationBar(dr, self)  # 初始化PicToolBar（本质为Wedgit），绑定到dr这个FigureCanvas上，然后将Toolbar绑到Layout上
        self.verticalLayout_5.addWidget(self.PicToolBar)
        self.graphicsView_2.setScene(self.scene)
        self.graphicsView_2.show()

    def select_tree_nodes(self):
        # tree_index = {'DQ': 0, 'Energy': 1, 'Launch': 2}
        s = self.treeWidget.currentItem().text(0)
        if s == 'Launch':
            self.show_data_edit_pictures(s)
        pass

    def select_tree3_nodes(self):
        tree_index = {'DQ': 0, 'Energy': 1}
        s = self.treeWidget_3.currentItem().text(0)
        try:
            self.change_tree_stackedwidgets_page(stackedwidgets_id=3, index_page=tree_index[s])
        except KeyError as e:  # 防止索引错误
            print(e)

    def add_combo_box(self):
        # button = QPushButton(u'测试', self)
        combo_box = QComboBox(self)
        self.verticalLayout_2.addWidget(combo_box)

    def button_clicked(self):
        self.MainProcess_thread = ThreadProcess(method='radar_cal_thread')
        self.MainProcess_thread.Message_Finish_2.connect(self.show_radar_pictures)
        self.MainProcess_thread.start()

    @QtCore.pyqtSlot()
    def compare_radar_pic(self):
        self.MainProcess_thread = ThreadProcess(method='radar_compare_thread')
        self.MainProcess_thread.Message_Finish_2.connect(self.show_radar_compare_pictures)
        self.MainProcess_thread.start()

    def datatableview_show(self, data_list):
        """
        Function of showing calculation results in data_table

        :param : data_list   List of result data to show (list)
        :return: -
        __author__ = 'Lu chao'
        __revised__ = 20171012
        """
        self.model = QtGui.QStandardItemModel(self.DatatableView)
        # self.model.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant('HH'))
        # self.model.setHeaderData(2, QtCore.Qt.Horizontal, QtCore.QVariant("FF"))
        for i in range(data_list.__len__()):
            for j in range(data_list[0].__len__()):
                self.model.setItem(i, j, QtGui.QStandardItem(data_list[i][j]))
        self.DatatableView.setModel(self.model)
        self.DatatableView.resizeColumnsToContents()

    def show_radar_pictures(self):
        dr2 = MyFigureCanvas(width=10, height=5, plot_type='2d-poly',
                             theta=self.MainProcess_thread.ax_holder_radar.theta,
                             data=self.MainProcess_thread.ax_holder_radar.data,
                             legends=self.MainProcess_thread.ax_holder_radar.legends)
        dr2.plot_radar_map_()
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(dr2)
        # self.PicToolBar = NavigationBar(dr, self)  # 初始化PicToolBar（本质为Wedgit），绑定到dr这个FigureCanvas上，然后将Toolbar绑到Layout上
        # self.gridLayout_5.addWidget(self.PicToolBar)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()

    def show_radar_compare_pictures(self):
        dr2 = MyFigureCanvas(width=3.5, height=5, plot_type='2d-poly',
                             theta=self.MainProcess_thread.ax_holder_radar.theta,
                             data=self.MainProcess_thread.ax_holder_radar.data,
                             legends=self.MainProcess_thread.ax_holder_radar.legends)
        dr2.plot_radar_map_()
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(dr2)
        # self.PicToolBar = NavigationBar(dr, self)  # 初始化PicToolBar（本质为Wedgit），绑定到dr这个FigureCanvas上，然后将Toolbar绑到Layout上
        # self.gridLayout_5.addWidget(self.PicToolBar)
        self.graphicsView_spider_compare.setScene(self.scene)
        self.graphicsView_spider_compare.show()


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

    def show_raw_data(self):
        pass

    def radar_cal_thread(self):
        try:
            self.ax_holder_radar = radar_plot(data=[68, 83, 90, 77, 89, 73], legends=['ZS11'])
            self.Message_Finish_2.emit('finish')
        except Exception as e:
            print(e)

    def radar_compare_thread(self):
        try:
            self.ax_holder_radar = radar_plot(data=[[68, 83, 90, 77, 89, 73], [65, 88, 92, 55, 82, 23]],
                                              legends=['AP31', 'ZS11'])
            self.Message_Finish_2.emit('finish')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ---------------QSS导入-------------------
    # file = QtCore.QFile('css.qss')
    # file.open(QtCore.QFile.ReadOnly)
    # stylesheet = file.readAll()
    # QtWidgets.QApplication.setStyleSheet(app, stylesheet.data().decode('utf-8'))  # utf-8  byte编码为String
    # ---------------实例化---------------------
    dlg = MainUiWindow()
    dlg.show()
    sys.exit(app.exec())
