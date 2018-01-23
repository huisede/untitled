#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2017/12/25 18:19
# @Author  :  LuChao
# @Site     : 
# @File     : Calculation_function.py
# @Software  : PyCharm


# -*- coding: utf8 -*-

import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import scipy.signal as signal
import peakutils


class SystemGain(object):
    """
    Main class of system gain, contains all the thing needed to be calculated or plotted.

    Contains：
    ******
    fun sg_main————Main function of calculating system gain, save  'self.sysGain_class'  to be called from UI.
    ******
    fun acc_response————Prepare acceleration response fig data
    fun launch————Prepare launch fig data
    fun max_acc————Prepare maximum acceleration fig data
    fun pedal_map————Prepare pedal map fig data
    fun shift_map————Prepare shift map fig data
    stc fun cut_sg_data_pedal————Data cutting function
    stc fun arm_interpolate————2-D interpolation method to generate system gain arm fig
    ******
    class AccResponse/Launch/MaxAcc/PedalMap/ShiftMap————Wrapper class of the corresponding fig
    class SystemGainDocker————A class that used to wrap all raw data and results
    ******
    fun plot_max_acc————Plotting method of generating maximum acceleration fig. NEED TO BE REWRITE IN Generate_Figs.py
    fun plot_pedal_map————Plotting method of generating pedal map fig. NEED TO BE REWRITE IN Generate_Figs.py
    fun plot_shift_map————Plotting method of generating shift map fig. NEED TO BE REWRITE IN Generate_Figs.py
    """

    def __init__(self, file_path):
        """
        Initial function of system gain.

        :param file_path: path of system gain file in local disc
        """
        self.filepath = file_path
        self.sysGain_class = {}

    def sg_main(self):
        '''
        Main function of calculating system gain, save  'self.sysGain_class'  to be called from UI.

        '''
        file_path = self.filepath
        # *******1-GetSysGainData******
        # 获取数据，判断数据类型，不同读取，获取文件名信息，
        SG_csv_Data_ful = pd.read_csv(file_path)
        # *******2-GetSGColumn*********
        # 获取列号，标准变量及面板输入，数据预处理
        SG_csv_Data_Selc = SG_csv_Data_ful.loc[:,
                           ['Time_abs', 'AccelActuPosHSC1', 'LongAccelG_M', 'VehSpdAvgNonDrvnHSC1',
                            'TrEstdGear_TCMHSC1', 'EnSpdHSC1', 'EnToqDrvrReqdExtdRngHSC1']]
        SG_csv_Data = SG_csv_Data_Selc.drop_duplicates()

        time_Data = SG_csv_Data['Time_abs'].tolist()
        pedal_Data = SG_csv_Data['AccelActuPosHSC1'].tolist()
        acc_Data = SG_csv_Data['LongAccelG_M'].tolist()
        vehSpd_Data = SG_csv_Data['VehSpdAvgNonDrvnHSC1'].tolist()
        gear_Data = SG_csv_Data['TrEstdGear_TCMHSC1'].tolist()
        enSpd_Data = SG_csv_Data['EnSpdHSC1'].tolist()
        torq_Data = SG_csv_Data['EnToqDrvrReqdExtdRngHSC1'].tolist()
        colour_Bar = ['orange', 'lightgreen', 'c', 'royalblue', 'lightcoral', 'yellow', 'red', 'brown',
                      'teal', 'blue', 'coral', 'gold', 'lime', 'olive']
        # 数据切分
        pedal_cut_index, pedal_avg = self.cut_sg_data_pedal(pedal_Data)
        # fig1三维图，增加最大加速度连线以及稳态车速线
        obj_AccResponse = self.acc_response(vehSpd_Data, acc_Data, pedal_cut_index, pedal_avg)  # 数据封装
        # # obj_AccResponse.plot_acc_response()
        # # fig2起步图，[5,10,20,30,40,50,100],后续补充判断大油门不是100也画出来,粗细
        obj_Launch = self.launch(acc_Data, pedal_Data, pedal_cut_index, pedal_avg)
        # # obj_Launch.plot_launch()
        obj_MaxAcc = self.max_acc(acc_Data, pedal_cut_index, pedal_avg)
        # obj_MaxAcc.plot_maxacc()
        # fig4 PedalMap-Gear
        obj_PedalMap = self.pedal_map(pedal_Data, enSpd_Data, torq_Data, pedal_cut_index, pedal_avg, colour_Bar)
        # obj_PedalMap.plot_pedal_map()
        # fig5 ShiftMap
        obj_ShiftMap = self.shift_map(pedal_Data, gear_Data, vehSpd_Data, pedal_cut_index, pedal_avg, colour_Bar)
        # obj_ShiftMap.plot_shift_map()
        self.sysGain_class = self.SystemGainDocker(obj_AccResponse, obj_Launch, obj_MaxAcc, obj_PedalMap, obj_ShiftMap,
                                                   SG_csv_Data_ful)

    def acc_response(self, vehspd_data, acc_data, pedal_cut_index, pedal_avg):
        acc_ped_map = [[], [], []]
        for i in range(0, len(pedal_avg)):
            iVehSpd = vehspd_data[pedal_cut_index[0][i]:pedal_cut_index[1][i]]
            iPed = [pedal_avg[i] * ix / ix for ix in range(pedal_cut_index[0][i], pedal_cut_index[1][i])]
            iAcc = acc_data[pedal_cut_index[0][i]:pedal_cut_index[1][i]]
            acc_ped_map[0].append(iPed)
            acc_ped_map[1].append(iVehSpd)
            acc_ped_map[2].append(iAcc)
        obj = self.AccResponse(acc_ped_map, pedal_avg)
        return obj

    def launch(self, acc_data, pedal_data, pedal_cut_index, pedal_avg):
        launch_map = [[], [], []]
        for i in range(0, len(pedal_avg)):
            if int(round(pedal_avg[i] / 5) * 5) in [10, 20, 30, 50, 100]:
                iTime = [0.05 * (ix - pedal_cut_index[0][i]) for ix in
                         range(pedal_cut_index[0][i], pedal_cut_index[0][i] + 100)]
                iAcc = acc_data[pedal_cut_index[0][i]:pedal_cut_index[0][i] + 100]
                launch_map[0].append(pedal_data[pedal_cut_index[0][i]:pedal_cut_index[0][i] + 100])
                launch_map[1].append(iAcc)
                launch_map[2].append(iTime)
            elif pedal_avg[i] == max(pedal_avg):
                iTime = [0.05 * (ix - pedal_cut_index[0][i]) for ix in
                         range(pedal_cut_index[0][i], pedal_cut_index[0][i] + 100)]
                iAcc = acc_data[pedal_cut_index[0][i]:pedal_cut_index[0][i] + 100]
                launch_map[0].append(pedal_data[pedal_cut_index[0][i]:pedal_cut_index[0][i] + 100])
                launch_map[1].append(iAcc)
                launch_map[2].append(iTime)
        obj = self.Launch(launch_map)
        return obj

    def max_acc(self, acc_data, pedal_cut_index, pedal_avg):
        acc_Ped_Max = []
        for i in range(0, len(pedal_avg)):
            acc_Ped_Max.append(max(acc_data[pedal_cut_index[0][i]:pedal_cut_index[0][i] + 1000]))
        obj = self.MaxAcc(pedal_avg, acc_Ped_Max)
        return obj

    def pedal_map(self, pedal_data, enSpd_data, torq_data, pedal_cut_index, pedal_avg, colour):
        pedal_map = [[], [], []]
        for i in range(0, len(pedal_avg)):
            iTorq = torq_data[pedal_cut_index[0][i]:pedal_cut_index[1][i]]
            iEnSpd = enSpd_data[pedal_cut_index[0][i]:pedal_cut_index[1][i]]
            pedal_map[0].extend(pedal_data[pedal_cut_index[0][i]:pedal_cut_index[1][i]])
            pedal_map[1].extend(iEnSpd)
            pedal_map[2].extend(iTorq)
        obj = self.PedalMap(pedal_map)
        return obj

    def shift_map(self, pedal_data, gear_data, vehspd_data, pedal_cut_index, pedal_avg, colour):
        shiftMap = [[], [], []]
        for i in range(1, max(gear_data)):
            # Gear上升沿下降沿
            for j in range(1, len(gear_data) - 1):
                if gear_data[j - 1] == i and gear_data[j] == i + 1:
                    for k in range(0, len(pedal_avg)):
                        if j > pedal_cut_index[0][k] and j < pedal_cut_index[1][k]:
                            shiftMap[0].append(gear_data[j - 1])
                            shiftMap[1].append(pedal_data[j - 1])
                            shiftMap[2].append(vehspd_data[j - 1])
        # 按档位油门车速排序
        shiftMap_Sort = sorted(np.transpose(shiftMap), key=lambda x: [x[0], x[1], x[2]])
        shiftMap_Data = np.transpose(shiftMap_Sort)
        obj = self.ShiftMap(shiftMap_Data)
        return obj

    @staticmethod
    def cut_sg_data_pedal(pedal_data):
        # 数据切分
        # edges detection initialize to avoid additional detection of rising edges/trailing edges
        pedal_data[0], pedal_data[-1] = 0, 0
        # end of edges detection initialize
        r_edge, t_edge = [], []
        # Pedal上升沿下降沿
        for i in range(1, len(pedal_data) - 1):

            if pedal_data[i - 1] == 0 and pedal_data[i] > 0:
                r_edge.append(i)
            if pedal_data[i + 1] == 0 and pedal_data[i] > 0:
                t_edge.append(i)
        # 判断个数大于1000个，判断重复pedal
        pedal_cut_index, pedal_avg = [[], []], []
        for j in range(0, len(r_edge)):
            if t_edge[j] - r_edge[j] > 1000:
                pedal_cut_index[0].append(r_edge[j])
                pedal_cut_index[1].append(t_edge[j])
                pedal_avg.append(np.mean(pedal_data[r_edge[j]:t_edge[j]]))
        return pedal_cut_index, pedal_avg

    @staticmethod
    def arm_interpolate(M):
        P = M[0]
        V = M[1]
        A = M[2]

        V_max = []  # 稳态车速
        V_inter = np.linspace(0, 120, 200)
        P_inter = []
        A_mesh = np.array([])

        for i in range(0, len(P)):
            iP = P[i]
            iV = V[i]
            iA = A[i]

            V_max.append(max(iV))  # 稳态车速
            P_inter.append(iP[0])  # 插曲面用到的pedal

            # 速度空白段加速度补零
            iV.append(max(iV))
            iA.append(0)
            iP.append(iP[0])
            iV.append(120)
            iA.append(0)
            iP.append(iP[0])

            # 固定速度网格插值
            accinter = interpolate.interp1d(iV, iA, kind='linear')
            A_inter = accinter(V_inter)
            if i == 0:
                A_mesh = A_inter
            else:
                A_mesh = np.vstack((A_mesh, A_inter))

        # 二维插值数据源检查
        # V_inter, P_inter = np.meshgrid(V_inter, P_inter)
        # fig = plt.figure()
        # ax1 = Axes3D(fig)
        # surf = ax1.plot_surface(V_inter, P_inter, A_mesh, rstride=2, cstride=2, cmap=cm.coolwarm, linewidth=0.5, antialiased=True)

        fitfunction1D = interpolate.interp1d(V_max, P_inter, kind='linear')
        fitfunction2D = interpolate.interp2d(V_inter, P_inter, A_mesh, kind='linear')
        # vehSpd_inter, pedal_inter = np.meshgrid(vehSpd_inter, pedal_inter)
        V_t = np.linspace(min(V_max), 120, 200)
        P_t = fitfunction1D(V_t)
        P_t = P_t + 25

        A_SG = []
        for i in range(0, len(V_t)):
            A_i = fitfunction2D(V_t[i], P_t[i])
            A_i = A_i.tolist()
            A_SG = A_SG + A_i
        fig6 = plt.figure()
        ax6 = fig6.add_subplot(111)
        ax6.plot(V_t, A_SG, color='green', linestyle='dashed', marker='*', markerfacecolor='blue',
                 markersize=8)
        ax6.grid(True, linestyle="--", color="k", linewidth="0.4")
        ax6.legend()
        axg6 = plt.gca()
        plt.xlim(0, 120)
        # plt.ylim(0, 0.03)
        axg6.set_xlabel('VehicleSpeed (km/h)', fontsize=12)
        axg6.set_ylabel('Acc (g)', fontsize=12)
        axg6.set_title('SystemGain', fontsize=12)
        return  # A_SG, V_t

    class AccResponse:
        def __init__(self, matrix, para1, parent=None, width=10, height=10, dpi=100, plot_type='3d'):
            self.xdata = matrix[1]
            self.ydata = matrix[0]
            self.zdata = matrix[2]
            self.data = matrix
            self.pedal_avg = para1
            self.plot_type = plot_type

            # def plot_acc_response(self):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画
            #     if self.plot_type == '2d':
            #         self.axes = self.fig.add_subplot(111)
            #     elif self.plot_type == '3d':
            #         self.axes = self.fig.add_subplot(111, projection='3d')
            #     for i in range(0, len(self.xdata)):
            #         self.axes.plot(self.xdata[i], self.ydata[i], self.zdata[i], label=int(round(self.pedal_avg[i] / 5) * 5))
            #         self.axes.legend()

    class Launch:
        def __init__(self, matrix):
            self.xdata = matrix[2]
            self.ydata = matrix[1]
            self.pedal = matrix[0]
            self.data = matrix

            # def plot_launch(self):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画
            #     fig2 = plt.figure()
            #     ax2 = fig2.add_subplot(111)
            #     for i in range(0, len(self.xdata)):
            #         ax2.plot(self.xdata[i], self.ydata[i], label=int(round(np.mean(self.pedal[i]) / 5) * 5))
            #         ax2.legend()
            #     ax2.grid(True, linestyle="--", color="k", linewidth="0.4")
            #     axg2 = plt.gca()
            #     axg2.set_xlabel('Time (s)', fontsize=12)
            #     axg2.set_ylabel('Acc (g)', fontsize=12)
            #     axg2.set_title('Launch', fontsize=12)

    class MaxAcc:
        def __init__(self, x, y):
            self.xdata = x
            self.ydata = y

            # def plot_maxacc(self):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画
            #     fig3 = plt.figure()
            #     ax3 = fig3.add_subplot(111)
            #     ax3.plot(self.xdata, self.ydata, color='green', linestyle='dashed', marker='o', markerfacecolor='blue',
            #              markersize=8)
            #     ax3.grid(True, linestyle="--", color="k", linewidth="0.4")
            #     ax3.legend()
            #     axg3 = plt.gca()
            #     axg3.set_xlabel('Pedal (%)', fontsize=12)
            #     axg3.set_ylabel('Acc (g)', fontsize=12)
            #     axg3.set_title('Acc-Pedal', fontsize=12)

    class PedalMap:
        def __init__(self, matrix):
            self.xdata = matrix[1]
            self.ydata = matrix[2]
            self.zdata = matrix[0]
            self.data = matrix

            # def plot_pedal_map(self):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画
            #     fig4 = plt.figure()
            #     ax4 = fig4.add_subplot(111)
            #     ax4.legend()
            #     fig_pedalmap = ax4.scatter(self.xdata, self.ydata, c=self.zdata, marker='o', linewidths=0.1,
            #                                s=6, cmap=plt.cm.get_cmap('RdYlBu_r'))
            #     plt.colorbar(fig_pedalmap)
            #     ax4.grid(True, linestyle="--", color="k", linewidth="0.4")
            #     axg4 = plt.gca()
            #     axg4.set_xlabel('Engine Speed (rpm)', fontsize=12)
            #     axg4.set_ylabel('Torque (Nm)', fontsize=12)
            #     axg4.set_title('PedalMap', fontsize=12)

    class ShiftMap:
        def __init__(self, matrix):
            self.xdata = matrix[2]
            self.ydata = matrix[1]
            self.gear = matrix[0]

            # def plot_shift_map(self):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画
            #     fig5 = plt.figure()
            #     ax5 = fig5.add_subplot(111)
            #     strLable = ['1->2', '2->3', '3->4', '4->5', '5->6', '6->7', '7->8', '8->9', '9->10']
            #     for i in range(1, int(max(self.gear)) + 1):
            #         # 选择当前Gear, color=colour[i]
            #         ax5.plot(self.xdata[np.where(self.gear == i)], self.ydata[np.where(self.gear == i)]
            #                  , marker='o', linestyle='-', linewidth=3, markerfacecolor='blue', markersize=4
            #                  , label=strLable[i - 1])
            #         ax5.legend()
            #     ax5.grid(True, linestyle="--", color="k", linewidth="0.4")
            #     axg5 = plt.gca()
            #     axg5.set_xlabel('Vehicle Speed (km/h)', fontsize=12)
            #     axg5.set_ylabel('Pedal (%)', fontsize=12)
            #     axg5.set_title('ShiftMap', fontsize=12)

    class SystemGainDocker:

        def __init__(self, accresponce, launch, maxacc, pedalmap, shiftmap, rawdata):
            self.accresponce = accresponce
            self.launch = launch
            self.maxacc = maxacc
            self.pedalmap = pedalmap
            self.shiftmap = shiftmap
            self.rawdata = rawdata

    def plot_max_acc(self, acc_data, pedal_cut_index, pedal_avg):   # 样例，不起作用
        # fig3起步特性图
        # acc_start=[0 0 0 0 7.5*100/51 7.5*100/51 7.5*100/51 7.5*100/51;0.02062 0.02709 0.03495 0.04371 0.14767 0.19659 0.24435 0.29176];
        # plot([acc_start(1,4),acc_start(1,5)],[acc_start(2,1),acc_start(2,5)],'b-');
        # plot([acc_start(1,4),acc_start(1,5)],[acc_start(2,2),acc_start(2,6)],'r-');
        # plot([acc_start(1,4),acc_start(1,5)],[acc_start(2,3),acc_start(2,7)],'g-');
        # plot([acc_start(1,4),acc_start(1,5)],[acc_start(2,4),acc_start(2,8)],'r-');
        # plot([7.5*100/51 7.5*100/51 7.5*100/51 7.5*100/51],acc_start(2,5:8),'r-');
        fig3 = plt.figure()
        ax3 = fig3.add_subplot(111)
        acc_Ped_Max = []
        for i in range(0, len(pedal_avg)):
            acc_Ped_Max.append(max(acc_data[pedal_cut_index[0][i]:pedal_cut_index[0][i] + 1000]))
        ax3.plot(pedal_avg, acc_Ped_Max, color='green', linestyle='dashed', marker='o', markerfacecolor='blue',
                 markersize=8)
        # , alpha="0.75"
        ax3.grid(True, linestyle="--", color="k", linewidth="0.4")
        ax3.legend()
        axg3 = plt.gca()
        axg3.set_xlabel('Pedal (%)', fontsize=12)
        axg3.set_ylabel('Acc (g)', fontsize=12)
        axg3.set_title('Acc-Pedal', fontsize=12)
        return pedal_avg, acc_Ped_Max

    def plot_pedal_map(self, pedal_data, enSpd_data, torq_data, pedal_cut_index, pedal_avg, colour):
        # fig4 PedalMap-Gear
        fig4 = plt.figure()
        ax4 = fig4.add_subplot(111)
        pedal_map = [[], [], []]
        # sc = plt.scatter(xy, xy, c=z, vmin=0, vmax=20, s=35, cmap=plt.cm.get_cmap('RdYlBu'))
        # plt.colorbar(sc)

        for i in range(0, len(pedal_avg)):
            iTorq = torq_data[pedal_cut_index[0][i]:pedal_cut_index[1][i]]
            iEnSpd = enSpd_data[pedal_cut_index[0][i]:pedal_cut_index[1][i]]
            # pedal_map[0].append(pedal_data[pedal_cut_index[0][i]:pedal_cut_index[1][i]])
            # pedal_map[1].append(iEnSpd)
            # pedal_map[2].append(iTorq)
            pedal_map[0].extend(pedal_data[pedal_cut_index[0][i]:pedal_cut_index[1][i]])
            pedal_map[1].extend(iEnSpd)
            pedal_map[2].extend(iTorq)
            # ax4.scatter(iEnSpd, iTorq, marker='o', linewidths=0.1, label=int(round(pedal_avg[i] / 5) * 5), s=10,
            #             c=colour[i])
            ax4.legend()
        fig_pedalmap = ax4.scatter(pedal_map[1], pedal_map[2], c=pedal_map[0], marker='o', linewidths=0.1,
                                   s=6, cmap=plt.cm.get_cmap('RdYlBu_r'))
        plt.colorbar(fig_pedalmap)
        ax4.grid(True, linestyle="--", color="k", linewidth="0.4")
        axg4 = plt.gca()
        axg4.set_xlabel('Engine Speed (rpm)', fontsize=12)
        axg4.set_ylabel('Torque (Nm)', fontsize=12)
        axg4.set_title('PedalMap', fontsize=12)
        # cm12 = plt.cm.get_cmap('RdYlBu')
        # xy = range(20)
        # z = xy
        # sc = plt.scatter(pedal_map[1], pedal_map[2], c=pedal_map[0], vmin=0, vmax=20, s=35, cmap=cm12)
        # plt.colorbar(sc)
        # plt.show()
        return pedal_map

    def plot_shift_map(self, pedal_data, gear_data, vehspd_data, pedal_cut_index, pedal_avg, colour):
        # fig5 ShiftMap
        shiftMap = [[], [], []]
        for i in range(1, max(gear_data)):
            # Gear上升沿下降沿
            for j in range(1, len(gear_data) - 1):
                if gear_data[j - 1] == i and gear_data[j] == i + 1:
                    for k in range(0, len(pedal_avg)):
                        if j > pedal_cut_index[0][k] and j < pedal_cut_index[1][k]:
                            shiftMap[0].append(gear_data[j - 1])
                            shiftMap[1].append(pedal_data[j - 1])
                            shiftMap[2].append(vehspd_data[j - 1])
        # 按档位油门车速排序
        shiftMap_Sort = sorted(np.transpose(shiftMap), key=lambda x: [x[0], x[1], x[2]])
        shiftMap_Data = np.transpose(shiftMap_Sort)
        fig5 = plt.figure()
        ax5 = fig5.add_subplot(111)
        strLable = ['1->2', '2->3', '3->4', '4->5', '5->6', '6->7', '7->8', '8->9', '9->10']

        for i in range(1, max(gear_data)):
            # 选择当前Gear, color=colour[i]
            ax5.plot(shiftMap_Data[2][np.where(shiftMap_Data[0] == i)], shiftMap_Data[1][np.where(shiftMap_Data[0] == i)]
                     , marker='o', linestyle='-', linewidth=3, markerfacecolor='blue', markersize=4
                     , label=strLable[i - 1])
            ax5.legend()
        ax5.grid(True, linestyle="--", color="k", linewidth="0.4")
        axg5 = plt.gca()
        axg5.set_xlabel('Vehicle Speed (km/h)', fontsize=12)
        axg5.set_ylabel('Pedal (%)', fontsize=12)
        axg5.set_title('ShiftMap', fontsize=12)
        return shiftMap_Data


class SpeedBump20(object):
    """
    Main class of SpeedBump20, contains all the thing needed to be calculated or plotted.
    ******
    the results of SpeedBump20 ：
    sr_impact, aftershake, sw_impact,ee_peak1, ee_peak2,obj_original_fig,obj_filter_fig
    ******
    the fun and class of SpeedBump20:
    fun sb_main————Main function of calculating speed bump, save  'self.sb_result'  to be called from UI.
    fun cut_sb_data_srx————Data cutting function
    stc fun cal_ee_peak————Calculate two value of peak-to-peak
    stc fun rms_cal————Calculate rms

    class OriginalFig/FilterFig————Wrapper class of the corresponding fig
    class SbResult————A class that used to wrap all raw data and results
    ******
    plot fun of SpeedBump20:
    stc fun plot_original_fig————Plotting method of original data fig. NEED TO BE REWRITE IN Generate_Figs.py
    stc fun plot_filter_fig————Plotting method of filter data fig. NEED TO BE REWRITE IN Generate_Figs.py
    """

    def __init__(self, file_path, fs):
        self.filepath = file_path
        self.fs = fs

        self.fig_original_data = {}
        self.fig_filter_data = {}
        self.table_result = pd.DataFrame()

    def sb_main(self):
        fs = self.fs
        sb_20_data_ful = pd.read_csv(self.filepath, skiprows=range(0, 12), header=1)
        sb_20_data_col = sb_20_data_ful.loc[:,
                         ['SR-X DIC24X013', 'SR-Y DIC24X014', 'SR-Z DIC24X015', 'SW-X DIC24X016', 'SW-Y DIC24X017',
                          'SW-Z DIC24X018', 'T']]
        sb_csv_data = sb_20_data_col.drop_duplicates()

        sr_x_data = np.array(sb_csv_data['SR-X DIC24X013'])
        sr_y_data = np.array(sb_csv_data['SR-Y DIC24X014'])
        sr_z_data = np.array(sb_csv_data['SR-Z DIC24X015'])
        time_data = np.array(sb_csv_data['T'])
        sw_x_data = np.array(sb_csv_data['SW-X DIC24X016'])
        sw_y_data = np.array(sb_csv_data['SW-Y DIC24X017'])
        sw_z_data = np.array(sb_csv_data['SW-Z DIC24X018'])
        self.original_data = self.OriginalData(time_data, sr_x_data, sr_y_data, sr_z_data,sw_x_data,sw_y_data,sw_z_data)
        [st, snd] = self.cut_sb_data_srx(sr_x_data)

        # 滤波
        b = signal.firwin(31, [1 * 2 / fs, 100 * 2 / fs], window=('kaiser', 0.5), pass_zero=False)
        sr_x_filter1 = signal.convolve(sr_x_data, b)
        sr_y_filter1 = signal.convolve(sr_y_data, b)
        sr_z_filter1 = signal.convolve(sr_z_data, b)
        w, gd = signal.group_delay((b, 1))
        n_delay = int(round(np.mean(gd)))
        st1 = int(round(st[0] + n_delay))
        snd1 = int(round(snd[0] + n_delay))
        self.filter_data = self.FilterData(sr_x_data, sr_y_data, sr_z_data, time_data, sw_x_data, sw_y_data,sw_z_data, st1, snd1, fs)

        sr_impact = []
        ee_peak1 = []
        ee_peak2 =[]
        after_shake = []
        sw_impact = []

        # SR_imapct计算
        vdv_x = sum([i ** 4 for i in sr_x_filter1[st1:snd1]])
        vdv_x = vdv_x ** 0.25
        vdv_y = sum([i ** 4 for i in sr_y_filter1[st1:snd1]])
        vdv_y = vdv_y ** 0.25
        vdv_z = sum([i ** 4 for i in sr_z_filter1[st1:snd1]])
        vdv_z = vdv_z ** 0.25
        sr_impact.append((vdv_x ** 2 + vdv_y ** 2 + vdv_z ** 2) ** 0.5)

        ee_peak11, ee_peak22 = self.cal_ee_peak(fs, sr_x_filter1, st1, snd1)
        ee_peak1.append(ee_peak11)
        ee_peak2.append(ee_peak22)

        # aftershake计算
        b2 = signal.firwin(16, [5 * 2 / fs, 30 * 2 / fs], window=('kaiser', 0.5), pass_zero=False)
        sr_x_filter2 = signal.convolve(sr_x_data, b2)
        sr_y_filter2 = signal.convolve(sr_y_data, b2)
        sr_z_filter2 = signal.convolve(sr_z_data, b2)
        w2, gd2 = signal.group_delay((b2, 1))
        n_delay2 = round(np.mean(gd2))
        st2 = int(st[0] + n_delay2)
        snd2 = int(snd[0] + n_delay2)
        rms_x = self.rms_cal(sr_x_filter2[st2:snd2])
        rms_y = self.rms_cal(sr_y_filter2[st2:snd2])
        rms_z = self.rms_cal(sr_z_filter2[st2:snd2])
        after_shake.append((rms_x ** 2 + rms_y ** 2 + rms_z ** 2) ** 0.5)

        # SW_Impact计算
        sw_x_filter1 = signal.convolve(sw_x_data, b)
        sw_y_filter1 = signal.convolve(sw_y_data, b)
        sw_z_filter1 = signal.convolve(sw_z_data, b)
        vdv_wx = sum([i ** 4 for i in sw_x_filter1[st1:snd1]])
        vdv_wx = vdv_wx ** 0.25
        vdv_wy = sum([i ** 4 for i in sw_y_filter1[st1:snd1]])
        vdv_wy = vdv_wy ** 0.25
        vdv_wz = sum([i ** 4 for i in sw_z_filter1[st1:snd1]])
        vdv_wz = vdv_wz ** 0.25
        sw_impact.append((vdv_wx ** 2 + vdv_wy ** 2 + vdv_wz ** 2) ** 0.5)

        self.sb_table_result = pd.DataFrame({'sr_impact': sr_impact, 'after_shake': after_shake, 'sw_impact': sw_impact,'ee_peak1': ee_peak1, 'ee_peak2': ee_peak2})

    @staticmethod
    def cal_ee_peak(fs, sr_x_filter1, st1, snd1):
        nn_delta = round(0.4 * fs)
        # 先找到所有峰值点
        sr_x_filter_cal = sr_x_filter1[st1:round(st1 / 2 + snd1 / 2)]
        indexes = peakutils.indexes(sr_x_filter_cal, thres=0.5, min_dist=30)
        indexes_sr_x = sorted(sr_x_filter_cal[indexes], reverse=True)
        max_sr_x1 = indexes_sr_x[0]
        index_max_sr_x1 = np.where(sr_x_filter_cal == max_sr_x1)
        max_sr_x2 = indexes_sr_x[1]
        index_max_sr_x2 = np.where(sr_x_filter_cal == max_sr_x2)
        index_max_sr_x = int(np.array(min(index_max_sr_x1, index_max_sr_x2)))

        max_sr_x = sr_x_filter_cal[index_max_sr_x]
        min_sr_x = min(sr_x_filter_cal[index_max_sr_x:index_max_sr_x + 100])
        index_min_sr_x = (sr_x_filter_cal[index_max_sr_x:snd1]).tolist().index(min_sr_x) + index_max_sr_x - 1
        ee_peak1 = max_sr_x - min_sr_x

        max_sr_x2 = max(sr_x_filter1[index_max_sr_x + nn_delta:snd1])
        index_max_sr_x2 = sr_x_filter1[index_max_sr_x + nn_delta:snd1].tolist().index(
            max_sr_x2) + index_max_sr_x + nn_delta - 1
        min_sr_x2 = min(sr_x_filter1[index_max_sr_x2:snd1])
        index_min_sr_x2 = (sr_x_filter1[index_max_sr_x:snd1]).tolist().index(min_sr_x2) + index_max_sr_x2 - 1
        ee_peak2 = max_sr_x2 - min_sr_x2
        return ee_peak1, ee_peak2

    @staticmethod
    def rms_cal(sr_x):
        length = len(sr_x)
        nn = np.array(sr_x)
        nn2 = nn * nn
        sum2 = nn2.sum()
        var = sum2 / length
        return var ** 0.5

    def cut_sb_data_srx(self, sr_x):
        # 对数据进行切割，找到满足条件的位置，这里将数据长度大于650的进行了删除
        # 手动截取功能暂未实现
        st = []
        snd = []
        nn = 0
        ll = len(sr_x)
        while nn < ll:
            active = True
            NN = 0
            while active:
                for i in range(1, 6):
                    rms = self.rms_cal(sr_x[nn + i - 1:nn + 9 + i - 1])
                    if rms > 0.3:
                        NN = NN + 1
                    else:
                        NN = 0
                if NN >= 4 or nn > ll:
                    active = False
                else:
                    nn = nn + 1
            if nn > 4000:
                aa = 1
            st.append(nn)
            NN = 0
            nn = nn + 400
            active = True
            while active:
                for i in range(1, 5):
                    rms = self.rms_cal(sr_x[nn:nn + 9])
                    if rms < 0.3:
                        NN = NN + 1
                    else:
                        NN = 0
                if NN >= 3 or nn > ll:
                    active = False
                else:
                    nn = nn + 1
            snd.append(nn)

        for i in range(1, len(st)):
            if snd[i] - st[i] > 650:
                snd.remove(snd(i))
                st.remove(st(i))
        return st, snd

    class SbResult:
        def __init__(self, sr_impact, after_shake, sw_impact, ee_peak1, ee_peak2, obj_original_fig, obj_filter_fig):
            self.sr_impact = sr_impact
            self.after_shake = after_shake
            self.sw_impact = sw_impact
            self.ee_peak1 = ee_peak1
            self.ee_peak2 = ee_peak2
            self.obj_original_fig = obj_original_fig
            self.obj_filter_fig = obj_filter_fig

    class OriginalData:
        def __init__(self, time_data, sr_x_data, sr_y_data, sr_z_data,sw_x_data,sw_y_data,sw_z_data):
            self.time_data = time_data
            self.sr_x_data = sr_x_data
            self.sr_y_data = sr_y_data
            self.sr_z_data = sr_z_data
            self.sw_x_data = sw_x_data
            self.sw_y_data = sw_y_data
            self.sw_z_data = sw_z_data

    class FilterData:
        def __init__(self, sr_x_filter, sr_y_filter, sr_z_filter, time_data, sw_x_filter, sw_y_filter, sw_z_filter, st1,snd1, fs):
            self.sr_x_data = sr_x_filter[st1 - 1 * fs:snd1 + 1 * fs]
            self.sr_y_data = sr_y_filter[st1 - 1 * fs:snd1 + 1 * fs]
            self.sr_z_data = sr_z_filter[st1 - 1 * fs:snd1 + 1 * fs]
            self.time_data = time_data[st1 - 1 * fs:snd1 + 1 * fs]
            self.sw_x_data = sw_x_filter[st1 - 1 * fs:snd1 + 1 * fs]
            self.sw_y_data = sw_y_filter[st1 - 1 * fs:snd1 + 1 * fs]
            self.sw_z_data = sw_z_filter[st1 - 1 * fs:snd1 + 1 * fs]
            self.st1 = st1
            self.snd1 = snd1

    @staticmethod
    def plot_original_fig(original_data):
        time_data = original_data.time_data
        sr_x_data = original_data.sr_x_data
        sr_y_data = original_data.sr_y_data
        sr_z_data = original_data.sr_z_data
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        ax1.plot(time_data, sr_x_data, color='black')
        ax1.plot(time_data, sr_y_data, color='red')
        ax1.plot(time_data, sr_z_data, color='blue')
        exam_x = np.where(sr_x_data > 10)
        exam_y = np.where(sr_y_data > 10)
        exam_z = np.where(sr_z_data > 10)

        if np.isnan(exam_x) == False:
            for nn in exam_x:
                ax1.plot(time_data[nn], sr_x_data[nn], color='red', marker='x', markersize=18)
                sr_x_data[nn] = 0
        if np.isnan(exam_y) == False:
            for nn in exam_y:
                ax1.plot(time_data[nn], sr_y_data[nn], color='red', marker='x', markersize=18)
        if np.isnan(exam_z) == False:
            for nn in exam_z:
                ax1.plot(time_data[nn], sr_z_data[nn], color='red', marker='x', markersize=18)
        ax1.set_xlabel('Time (s)', fontsize=20)
        ax1.set_ylabel('Acc (g)', fontsize=20)
        ax1.set_title('Speed bump 20kph', fontsize=20)
        plt.show()

    @staticmethod
    def plot_filter_fig(filter_data):
        # fig2截取数据的图片
        time_data = filter_data.time_data
        sr_x_filter = filter_data.sr_x_data
        sr_y_filter = filter_data.sr_y_data
        sr_z_filter = filter_data.sr_z_data
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        ax2.plot(time_data, sr_x_filter, color='black')
        ax2.plot(time_data, sr_y_filter, color='red')
        ax2.plot(time_data, sr_z_filter, color='blue')
        ax2.set_xlabel('Time (s)', fontsize=20)
        ax2.set_ylabel('Acc (g)', fontsize=20)
        ax2.set_title('Speed bump 20kph', fontsize=20)
        plt.show()


class RatingMap(object):
    def __init__(self, theta, data, legends):
        self.theta = theta
        self.data = data
        self.legends = legends


def rating_map(theta, data, legends):
    obj = RatingMap(theta, data, legends)
    return obj


def radar_plot(data, legends):
    '''
    plot radar fig of total rating.

    :param data: import data   list
    :param legends:  figure legends    list[str]
    :return: none
    '''
    # 生成测试数
    try:
        isinstance(data, list)
    except Exception as e:
        print(e)

    data = np.array(data)
    if data.size == 6:
        theta = np.linspace(0, 2 * np.pi, len(data), endpoint=False)
        # 数据预处理
        data = np.concatenate((data, [data[0]]))
        theta = np.concatenate((theta, [theta[0]]))
    else:
        theta = np.linspace(0, 2 * np.pi, data.shape[1], endpoint=False)
        data = np.concatenate((data, np.array([data[:, 0]]).T), axis=1)
        theta = np.concatenate((theta, [theta[0]]))
    # 画图方式
    obj_ratingmap = rating_map(theta, data, legends)

    return obj_ratingmap


if __name__ == '__main__':
    # *******1-GetSysGainData****** AS22_C16UVV016_SystemGain_20160925_D_M_SL, IP31_L16UOV055_10T_SystemGain_20160225
    a = SystemGain('./IP31_L16UOV055_Ride_SyGa_20160225_SL.csv')
    a.sg_main()
    plt.show()

    print('Finish!')
