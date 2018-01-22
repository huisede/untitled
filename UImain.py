#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#  @Time     : 2017/12/6 11:15
#  @Author  :  LuChao
#  @Site     : 
#  @File     : UImain.py
#  @Software  : PyCharm

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from Ui_VI_Accessment_System import Ui_VI_Accessment_System  # 界面源码
from Generate_Figs import *  # 绘图函数
from Calculation_function_ import *   # 计算函数


class MainUiWindow(QMainWindow, Ui_VI_Accessment_System):

    def __init__(self, parent=None):
        super(MainUiWindow, self).__init__(parent)
        self.setupUi(self)
        self.initial()

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

    # ---------------------------- 初始化 -----------------------------------------
    def initial(self):
        self.graphicsView_2 = MyQtGraphicView(self.page_dataedit)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.verticalLayout_5.addWidget(self.graphicsView_2)
        self.graphicsView_2.Message_Drag_accept.connect(self.show_data_edit_drag_pictures)   # 拖拽重绘
        self.graphicsView_2.Message_DoubleClick.connect(self.highlight_signal)  # 双击高亮

    # ---------------------------- 右键菜单 -----------------------------------------

    def createContextMenu_RawDataView(self):
        '''

        :return:
        '''
        self.graphicsView_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.graphicsView_2.customContextMenuRequested.connect(lambda: self.showContextMenu('graphicsView_2'))
        self.graphicsView_2.contextMenu = QtWidgets.QMenu(self)
        self.graphicsView_2.actionA = self.graphicsView_2.contextMenu.addAction(QtGui.QIcon("images/0.png"), u'|  标记')
        self.graphicsView_2.actionA.triggered.connect(self.select_marker)

        # 添加二级菜单
        self.graphicsView_2.second = self.graphicsView_2.contextMenu.addMenu(QtGui.QIcon("images/0.png"), u"|  二级菜单")
        self.graphicsView_2.actionD = self.graphicsView_2.second.addAction(QtGui.QIcon("images/0.png"), u'|  动作A')
        self.graphicsView_2.actionE = self.graphicsView_2.second.addAction(QtGui.QIcon("images/0.png"), u'|  动作B')
        self.graphicsView_2.actionF = self.graphicsView_2.second.addAction(QtGui.QIcon("images/0.png"), u'|  动作C')

        return

    def createContextMenu_sg_fig_view(self):
        '''

        :return:
        '''
        self.graphicsView_3.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.graphicsView_3.customContextMenuRequested.connect(lambda: self.showContextMenu('graphicsView_3'))
        self.graphicsView_3.contextMenu = QtWidgets.QMenu(self)
        self.graphicsView_3.actionA = self.graphicsView_3.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u'| 加速度相应曲面')
        self.graphicsView_3.actionB = self.graphicsView_3.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u"| 起步特性")
        self.graphicsView_3.actionC = self.graphicsView_3.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u"| Pedal Map")
        self.graphicsView_3.actionD = self.graphicsView_3.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u"| Shift Map")
        self.graphicsView_3.actionE = self.graphicsView_3.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u"| 香蕉图")
        self.graphicsView_3.actionA.triggered.connect(lambda: self.change_handle_pictures('accresp',
                                                                                          'PicToolBar_1',
                                                                                          'graphicsView_3',
                                                                                          'gridLayout_5'))
        self.graphicsView_3.actionB.triggered.connect(lambda: self.change_handle_pictures('launch',
                                                                                          'PicToolBar_1',
                                                                                          'graphicsView_3',
                                                                                          'gridLayout_5'))
        self.graphicsView_3.actionC.triggered.connect(lambda: self.change_handle_pictures('Pedal Map',
                                                                                          'PicToolBar_1',
                                                                                          'graphicsView_3',
                                                                                          'gridLayout_5'))

        self.graphicsView_4.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.graphicsView_4.customContextMenuRequested.connect(lambda: self.showContextMenu('graphicsView_4'))
        self.graphicsView_4.contextMenu = QtWidgets.QMenu(self)
        self.graphicsView_4.actionA = self.graphicsView_4.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u'| 加速度相应曲面')
        self.graphicsView_4.actionB = self.graphicsView_4.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u"| 起步特性")
        self.graphicsView_4.actionC = self.graphicsView_4.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u"| Pedal Map")
        self.graphicsView_4.actionD = self.graphicsView_4.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u"| Shift Map")
        self.graphicsView_4.actionE = self.graphicsView_4.contextMenu.addAction(QtGui.QIcon("./Image/DataIcon.png"), u"| 香蕉图")
        self.graphicsView_4.actionA.triggered.connect(lambda: self.change_handle_pictures('accresp',
                                                                                          'PicToolBar_2',
                                                                                          'graphicsView_4',
                                                                                          'gridLayout_17'))
        self.graphicsView_4.actionB.triggered.connect(lambda: self.change_handle_pictures('launch',
                                                                                          'PicToolBar_2',
                                                                                          'graphicsView_4',
                                                                                          'gridLayout_17'))
        self.graphicsView_4.actionC.triggered.connect(lambda: self.change_handle_pictures('Pedal Map',
                                                                                          'PicToolBar_2',
                                                                                          'graphicsView_4',
                                                                                          'gridLayout_17'))

    def showContextMenu(self, handle):
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        eval('self.'+handle+'.contextMenu.exec_(QtGui.QCursor.pos())')  # 在鼠标位置显示
        print(QtGui.QCursor.pos())
        # self.contextMenu.show()

    # ---------------------------- 回调函数 -----------------------------------------
    # -----|主菜单
    def load_sysgain_data(self):
        filepath = QFileDialog.getOpenFileName(self, filter='*.csv')
        filepath_full = filepath[0]
        self.MainProcess_thread = ThreadProcess(method='sg_cal_thread', filepath=filepath_full)
        self.MainProcess_thread.Message_Finish.connect(self.show_ax_pictures)
        self.MainProcess_thread.start()

    # -----|--|主页面
    def change_main_page(self, index_page):
        self.stackedWidget.setCurrentIndex(index_page)

    def change_tree_stackedwidgets_page(self, stackedwidgets_id, index_page):
        eval('self.stackedWidget_' + str(stackedwidgets_id) + '.setCurrentIndex(index_page)')

    # -----|--|Overall Widget 页面
    def add_combo_box(self):
        # button = QPushButton(u'测试', self)
        combo_box = QComboBox(self)
        self.verticalLayout_2.addWidget(combo_box)

    def button_clicked(self):
        self.MainProcess_thread = ThreadProcess(method='radar_cal_thread')
        self.MainProcess_thread.Message_Finish_2.connect(self.show_radar_pictures)
        self.MainProcess_thread.start()

    def show_radar_pictures(self):
        '''
        Function to show main rating radar pictures

        :return:
        '''
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

    # -----|--|Data Edit 页面
    @QtCore.pyqtSlot(dict)
    def show_data_edit_pictures(self, dict_in):  # 原始数据编辑界面
        '''

        :param dict_in: Contains the specific input of the signal to plot
                        [fig_name(mostly same as signal_name), signal_name, Navigation bar needed? T/F]
        :return:
        '''
        raw_index = {'VehicleSpd': 'VehSpdAvgNonDrvnHSC1',
                     'AccPed': 'AccelActuPosHSC1',
                     'LongtiAcc': 'LongAccelG_M',
                     'time': 'Time_abs'}
        try:
            self.dr = MyFigureCanvas(width=16, height=8, plot_type='2d-multi',
                                     title=dict_in['title'])
            self.dr.plot_raw_data(time=self.MainProcess_thread.ax_holder_SG.sysGain_class.rawdata[raw_index['time']].tolist(),
                                  raw_data=self.MainProcess_thread.ax_holder_SG.sysGain_class.rawdata[raw_index[dict_in['data']]].tolist(),
                                  legend=[dict_in['data']])

            self.scene = QtWidgets.QGraphicsScene()
            self.scene.addWidget(self.dr)
            if dict_in['Nvbar']:
                self.PicToolBar = NavigationBar(self.dr, self)
                # 初始化PicToolBar（本质为Wedgit），绑定到dr这个FigureCanvas上，然后将Toolbar绑到Layout上
                self.verticalLayout_5.addWidget(self.PicToolBar)

            self.graphicsView_2.setScene(self.scene)
            self.graphicsView_2.setUpdatesEnabled(True)
            self.graphicsView_2.setViewportUpdateMode(0)
            self.graphicsView_2.show()

            self.dr.mpl_connect('button_press_event', self.get_mouse_xy_plot)
        except Exception as e:
            print(e)

    @QtCore.pyqtSlot(dict)
    def show_data_edit_drag_pictures(self, dict_in):
        raw_index = {'VehicleSpd': 'VehSpdAvgNonDrvnHSC1',
                     'AccPed': 'AccelActuPosHSC1',
                     'LongtiAcc': 'LongAccelG_M',
                     'time': 'Time_abs'}
        try:
            self.PicToolBar.home()
            self.dr.plot_raw_data(time=self.MainProcess_thread.ax_holder_SG.sysGain_class.rawdata[raw_index['time']].tolist(),
                                  raw_data=self.MainProcess_thread.ax_holder_SG.sysGain_class.rawdata[raw_index[dict_in['data']]].tolist(),
                                  legend=[dict_in['data']])
        except Exception as e:
            print(e)

    def select_marker(self):
        QtCore.Qt.Key_Left
        pass

    def highlight_signal(self):

        pass

    def select_tree_nodes(self):
        # tree_index = {'DQ': 0, 'Energy': 1, 'Launch': 2}
        s = self.treeWidget.currentItem().text(0)
        if s == 'Launch':
            self.show_data_edit_pictures({'title': s, 'data': 'AccPed', 'Nvbar': True})
        pass

    def get_mouse_xy_plot(self, event):
        self.xyCoordinates = [event.xdata, event.ydata]  # 捕捉鼠标点击的坐标
        print(self.xyCoordinates)

    # -----|--|Rating Details 页面
    # -----|--|--|System Gain
    def show_ax_pictures(self):  # System Gain 初始绘图函数

        # self.createContextMenu_sg_fig_view()

        dr = MyFigureCanvas(width=6, height=4, plot_type='3d',
                            data=self.MainProcess_thread.ax_holder_SG.sysGain_class.accresponce.data,
                            pedal_avg=self.MainProcess_thread.ax_holder_SG.sysGain_class.accresponce.pedal_avg)
        dr.plot_acc_response_()
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(dr)
        try:
            if self.gridLayout_5.itemAt(0):   # 如果已经有NVbar,删掉后重新捆绑
                self.gridLayout_5.itemAt(0).widget().deleteLater()
                self.gridLayout_5.removeWidget(self.gridLayout_5.itemAt(0).widget())
            else:
                self.createContextMenu_sg_fig_view()  # 第一次初始化右键菜单，一次把两个canvas的菜单都初始化了  ！！！
            self.PicToolBar_1 = NavigationBar(dr, self)
            # 初始化PicToolBar（本质为Wedgit），绑定到dr这个FigureCanvas上，然后将Toolbar绑到Layout上
            self.gridLayout_5.addWidget(self.PicToolBar_1)
            self.graphicsView_3.setScene(self.scene)
            self.graphicsView_3.show()
        except Exception as e:
            print(e)

        dr_launch_ = MyFigureCanvas(width=6, height=4, plot_type='2d',
                                    data=self.MainProcess_thread.ax_holder_SG.sysGain_class.launch.data)
        dr_launch_.plot_launch_()
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(dr_launch_)
        try:
            if self.gridLayout_17.itemAt(0):
                self.gridLayout_17.itemAt(0).widget().deleteLater()
                self.gridLayout_17.removeWidget(self.gridLayout_17.itemAt(0).widget())
            self.PicToolBar_2 = NavigationBar(dr_launch_, self)
            # 初始化PicToolBar（本质为Wedgit），绑定到dr这个FigureCanvas上，然后将Toolbar绑到Layout上
            self.gridLayout_17.addWidget(self.PicToolBar_2)
            self.graphicsView_4.setScene(self.scene)
            self.graphicsView_4.show()
        except Exception as e:
            print(e)

    def change_handle_pictures(self, pichandle, toolbar, graphicview, layout):  # SG切换图片
        if pichandle == 'Pedal Map':
            dr = MyFigureCanvas(width=6, height=4, plot_type='2d',
                                data=self.MainProcess_thread.ax_holder_SG.sysGain_class.pedalmap.data)
            dr.plot_pedal_map_()

        elif pichandle == 'launch':
            dr = MyFigureCanvas(width=6, height=4, plot_type='2d',
                                data=self.MainProcess_thread.ax_holder_SG.sysGain_class.launch.data)
            dr.plot_launch_()

        elif pichandle == 'accresp':
            dr = MyFigureCanvas(width=6, height=4, plot_type='3d',
                                data=self.MainProcess_thread.ax_holder_SG.sysGain_class.accresponce.data,
                                pedal_avg=self.MainProcess_thread.ax_holder_SG.sysGain_class.accresponce.pedal_avg)
            dr.plot_acc_response_()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(dr)
        # self.gridLayout_5.itemAt(0).widget()
        try:
            eval('self.' + layout + '.removeWidget(self.' + toolbar + ')')
            eval('self.' + toolbar + '.deleteLater()')
            exec('self.' + toolbar + '= NavigationBar(dr, self)')
            eval('self.' + layout + '.addWidget(self.' + toolbar + ')')
            eval('self.' + graphicview + '.setScene(self.scene)')
            eval('self.' + graphicview + '.show()')
        except Exception as e:
            print(e)
            print('From function：change_handle_pictures')
        pass

    # -----|--|Settings 页面
    def select_tree3_nodes(self):
        tree_index = {'DQ': 0, 'Energy': 1}
        s = self.treeWidget_3.currentItem().text(0)
        try:
            self.change_tree_stackedwidgets_page(stackedwidgets_id=3, index_page=tree_index[s])
        except KeyError as e:  # 防止索引错误
            print(e)

    # -----|--|Comparison 页面
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
        self.ax_holder_SG = SystemGain(file_path=self.kwargs['filepath'])
        self.ax_holder_SG.sg_main()
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


class MyQtGraphicView(QtWidgets.QGraphicsView):
    Message_Drag_accept = QtCore.pyqtSignal(dict)
    Message_DoubleClick = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyQtGraphicView, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        print(e.mimeData().text())
        self.Message_Drag_accept.emit({'title': e.mimeData().text(),
                                       'data': e.mimeData().text(),
                                       'Nvbar': False})

    def mouseDoubleClickEvent(self, e):
        self.Message_DoubleClick.emit(1)


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
