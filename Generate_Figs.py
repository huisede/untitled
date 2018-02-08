import matplotlib
import numpy as np

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationBar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm


# import warnings
# warnings.filterwarnings("ignore")


# ----------------------------
# class definition


class MyFigureCanvas(FigureCanvas):
    """
    Main class of generating figs in GUI using matplot.backend_qt5agg

    Contains:
    drawing functions
        plot_acc_response_
        plot_launch_
        plot_max_acc_
        plot_pedal_map_
        plot_raw_data
        plot_radar_map_
    test function
        test
    """

    def __init__(self, parent=None, width=10, height=10, dpi=100, plot_type='3d', **kwargs):
        self.fig = Figure(figsize=(width, height), dpi=100)
        super(MyFigureCanvas, self).__init__(self.fig)
        self.kwargs = kwargs
        # self.data = data
        # self.parameter1 = para1
        # FigureCanvas.__init__(self, fig)  # 初始化父类   堆栈溢出问题！
        # self.setParent(parent)
        if plot_type == '2d':
            self.axes = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        elif plot_type == '3d':
            self.axes = self.fig.add_subplot(111, projection='3d')
        elif plot_type == '2d-poly':
            self.axes = self.fig.add_subplot(111, polar=True)
        elif plot_type == '2d-multi':
            self.i = 0

    def plot_acc_response(self, data, ped_avg):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画

        for i in range(0, len(data[1])):
            self.axes.plot(data[1][i], data[0][i], data[2][i], label=int(round(ped_avg[i] / 5) * 5))
            self.axes.legend(bbox_to_anchor=(1.02, 1), loc=1, borderaxespad=0)
            self.axes.set_xlabel('Velocity (kph)', fontsize=12)
            self.axes.set_ylabel('Pedal (%)', fontsize=12)
            self.axes.set_zlabel('Acc (g) ', fontsize=12)

    def plot_launch(self, data):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画

        for i in range(0, len(data[2])):
            self.axes.plot(data[2][i], data[1][i], label=int(round(np.mean(data[0][i]) / 5) * 5))
            self.axes.legend()
            self.axes.grid(True, linestyle="--", color="k", linewidth="0.4")
        self.axes.set_xlabel('Time (s)', fontsize=12)
        self.axes.set_ylabel('Acc (g)', fontsize=12)
        self.axes.set_title('Launch', fontsize=12)

    def plot_maxacc(self, data):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画

        self.axes.plot(data[0], data[1], color='green', linestyle='dashed', marker='o', markerfacecolor='blue',
                       markersize=8)
        self.axes.grid(True, linestyle="--", color="k", linewidth="0.4")
        self.axes.legend()
        self.axes.set_xlabel('Pedal (%)', fontsize=12)
        self.axes.set_ylabel('Acc (g)', fontsize=12)
        self.axes.set_title('Acc-Pedal', fontsize=12)

    def plot_pedal_map(self, data):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画

        pedalmap = self.axes.scatter(data[1], data[2], c=data[0], marker='o', linewidths=0.1,
                                     s=6, cmap=cm.get_cmap('RdYlBu_r'))
        self.axes.grid(True, linestyle="--", color="k", linewidth="0.4")
        self.axes.set_xlabel('Engine Speed (rpm)', fontsize=12)
        self.axes.set_ylabel('Torque (Nm)', fontsize=12)
        self.axes.set_title('PedalMap', fontsize=12)

    def plot_shift_map(self, data):  # 目前做不到先画图，后统一输出，只能在主线程里面同步画

        str_label = ['1->2', '2->3', '3->4', '4->5', '5->6', '6->7', '7->8', '8->9', '9->10']
        for i in range(1, int(max(data[0])) + 1):
            # 选择当前Gear, color=colour[i]
            self.axes.plot(data[2][np.where(data[0] == i)], data[1][np.where(data[0] == i)]
                           , marker='o', linestyle='-', linewidth=3, markerfacecolor='blue', markersize=4
                           , label=str_label[i - 1])
            self.axes.legend()
        self.axes.grid(True, linestyle="--", color="k", linewidth="0.4")
        self.axes.set_xlabel('Vehicle Speed (km/h)', fontsize=12)
        self.axes.set_ylabel('Pedal (%)', fontsize=12)
        self.axes.set_title('ShiftMap', fontsize=12)

    def plot_systemgain_curve(self, vehspd_sg, acc_sg):
        speedIndex = np.arange(10, 170, 10)
        speedIndex = speedIndex.tolist()
        acc_banana = np.zeros((5, len(speedIndex)))
        acc_banana[0, :] = [0.0144, 0.0126, 0.0111, 0.0097, 0.0084, 0.0073, 0.0064, 0.0056, 0.0048,
                            0.0042, 0.0037, 0.0032, 0.0028, 0.0024, 0.0021, 0.0018]
        acc_banana[1, :] = [0.0172, 0.0152, 0.0134, 0.0119, 0.0104, 0.0092, 0.0081, 0.0071, 0.0063,
                            0.0055, 0.0049, 0.0043, 0.0038, 0.0034, 0.0030, 0.0026]
        acc_banana[2, :] = [0.0200, 0.0178, 0.0158, 0.0141, 0.0125, 0.0111, 0.0098, 0.0087, 0.0078,
                            0.0069, 0.0062, 0.0055, 0.0049, 0.0043, 0.0038, 0.0033]
        acc_banana[3, :] = [0.0228, 0.0204, 0.0182, 0.0163, 0.0145, 0.0129, 0.0115, 0.0103, 0.0092,
                            0.0082, 0.0074, 0.0066, 0.0059, 0.0053, 0.0047, 0.0042]
        acc_banana[4, :] = [0.0256, 0.0230, 0.0206, 0.0185, 0.0166, 0.0149, 0.0133, 0.0119, 0.0107,
                            0.0096, 0.0086, 0.0077, 0.0069, 0.0062, 0.0055, 0.0049]

        self.axes.plot(vehspd_sg, acc_sg, color='green', linestyle='-')
        self.axes.plot(speedIndex, acc_banana[0, :], color='blue', linestyle='--')
        self.axes.plot(speedIndex, acc_banana[1, :], color='red', linestyle='--')
        self.axes.plot(speedIndex, acc_banana[2, :], color='black', linestyle='--')
        self.axes.plot(speedIndex, acc_banana[3, :], color='blue', linestyle='--')
        self.axes.plot(speedIndex, acc_banana[4, :], color='red', linestyle='--')
        self.axes.plot([speedIndex[0]] * 5, acc_banana[:, 0], color='blue', linestyle='-')
        self.axes.set_xlabel('velocity(km/h)')
        self.axes.set_ylabel('acc(g/mm)')
        self.axes.set_xlim(0, 120)
        self.axes.set_ylim(0, 0.03)
        self.axes.grid(True, linestyle="-", color="grey", linewidth="0.4")

    def plot_constant_speed(self, vehspd_cs, pedal_cs):

        self.axes.plot(vehspd_cs, pedal_cs, color='green', linestyle='dashed', marker='o', markerfacecolor='blue',
                       markersize=8)
        self.axes.grid(True, linestyle="--", color="k", linewidth="0.4")
        self.axes.legend()
        self.axes.set_xlabel('velocity (kph)', fontsize=12)
        self.axes.set_ylabel('pedal (%)', fontsize=12)
        self.axes.set_title('Constant Speed', fontsize=12)

    def plot_acc_response_(self):
        '''


        :return:
        '''
        self.xdata = self.kwargs['data'][1]
        self.ydata = self.kwargs['data'][0]
        self.zdata = self.kwargs['data'][2]
        self.pedal_avg = self.kwargs['pedal_avg']
        for i in range(0, len(self.xdata)):
            self.axes.plot(self.xdata[i], self.ydata[i], self.zdata[i], label=int(round(self.pedal_avg[i] / 5) * 5))
            self.axes.legend(bbox_to_anchor=(1.02, 1), loc=1, borderaxespad=0)
        self.axes.set_xlabel('Vehicle Speed (km/h)', fontsize=12)
        self.axes.set_ylabel('Pedal(%)', fontsize=12)
        self.axes.set_zlabel('Acc (g)', fontsize=12)
        self.axes.set_title('Acc-3D Map', fontsize=12)

    def plot_launch_(self):
        self.xdata = self.kwargs['data'][2]
        self.ydata = self.kwargs['data'][1]
        self.pedal = self.kwargs['data'][0]
        for i in range(0, len(self.xdata)):
            self.axes.plot(self.xdata[i], self.ydata[i], label=int(round(np.mean(self.pedal[i]) / 5) * 5))
            self.axes.legend()
        self.axes.grid(True, linestyle="--", color="k", linewidth="0.4")
        self.axes.set_xlabel('Time (s)', fontsize=12)
        self.axes.set_ylabel('Acc (g)', fontsize=12)
        self.axes.set_title('Launch', fontsize=12)

    def plot_max_acc_(self):
        self.xdata = self.kwargs['xdata']
        self.ydata = self.kwargs['ydata']
        self.axes.plot(self.xdata, self.ydata, color='green', linestyle='dashed', marker='o', markerfacecolor='blue',
                       markersize=8)
        self.axes.grid(True, linestyle="--", color="k", linewidth="0.4")
        self.axes.legend()
        self.axes.set_xlabel('Pedal (%)', fontsize=12)
        self.axes.set_ylabel('Acc (g)', fontsize=12)
        self.axes.set_title('Acc-Pedal', fontsize=12)

    def plot_pedal_map_(self):
        self.xdata = self.kwargs['data'][1]
        self.ydata = self.kwargs['data'][2]
        self.zdata = self.kwargs['data'][0]
        self.axes.scatter(self.xdata, self.ydata, c=self.zdata, marker='o', linewidths=0.1,
                          s=6, cmap=cm.get_cmap('RdYlBu_r'))
        self.axes.grid(True, linestyle="--", color="k", linewidth="0.4")
        self.axes.set_xlabel('Engine Speed (rpm)', fontsize=12)
        self.axes.set_ylabel('Torque (Nm)', fontsize=12)
        self.axes.set_title('PedalMap', fontsize=12)

    def test(self):
        x = [1, 2, 3]
        y = [2, 3, 5]
        z = [2, 1, 4]
        self.axes.scatter(x, y, z)

    def plot_raw_data(self, **kwargs):
        '''

        :param kwargs:
        :return:
        '''

        pos = [0.02, 0.1, 0.8, 0.8]
        colors = ['r', 'b', 'g', 'y']
        font_size = 10

        if self.i == 0:
            self.axes = self.fig.add_axes(pos, axisbg='w', label=kwargs['legend'])  # 设置初始的图层底色为白色
            self.axes.tick_params(axis='x', colors='black', labelsize=10)
            self.axes.set_xlabel('time (s)', fontsize=12)
        else:
            self.axes = self.fig.add_axes(pos, axisbg='none', label=kwargs['legend'])  # 设置随后的图层底色为透明
            # self.axes.set_xticks([])   #写完后去掉注释

        self.raw_data = kwargs['raw_data']  # 注意！！！！
        self.time = kwargs['time']
        self.fig_title = self.kwargs['title']
        self.axes.spines['right'].set_position(('outward', 60 * self.i))  # 图的右侧边框向外移动
        self.axes.spines['right'].set_color(colors[self.i])
        self.axes.spines['right'].set_linewidth(2)
        self.axes.plot(self.time, self.raw_data, linewidth=1, color=colors[self.i])
        self.axes.yaxis.set_ticks_position('right')
        self.axes.tick_params(axis='y', colors=colors[self.i])
        self.axes.set_ylabel(kwargs['legend'], fontsize=font_size, color=colors[self.i])
        self.axes.yaxis.set_label_position("right")
        # self.axes.grid()
        self.i += 1

        # self.axes.plot(self.raw_data)
        # self.axes.set_title(self.fig_title)
        # self.axes.set_ylabel('VehicleSpd (km/h)', fontsize=12)
        # self.axes.lines[-1].set_label(kwargs['legend'])  # 将最近添加的那根曲线命名
        # self.axes.grid(True)
        # self.axes.legend(kwargs['legend'])

    def plot_radar_map_(self):
        self.theta = self.kwargs['theta']
        self.data = self.kwargs['data']
        self.legends = self.kwargs['legends']
        # plt.thetagrids(theta*(180/np.pi), labels=labels, fontproperties=myfont)
        self.axes.set_ylim(0, 100)
        colour_Bar = ['blue', 'red', 'c', 'royalblue', 'lightcoral', 'yellow', 'lightgreen', 'brown',
                      'teal', 'orange', 'coral', 'gold', 'lime', 'olive']
        if self.data.size <= 7:  # 一条数据绘制
            # 画雷达图,并填充雷达图内部区域
            self.axes.plot(self.theta, self.data, "o-", color='blue', linewidth=2)
            self.axes.fill(self.theta, self.data, color="blue", alpha=0.25)
            self.axes.set_rgrids(np.arange(20, 100, 20), labels=np.arange(20, 100, 20), angle=0)
            self.axes.set_thetagrids(self.theta * (180 / np.pi), labels=np.array(["A", "B", "C", "D", "E", "F"]))
            self.axes.set_title("Rating")
        else:
            for i in range(self.data.size // 7):
                self.axes.plot(self.theta, self.data[i], 'o-', color=colour_Bar[i], linewidth=2)
                self.axes.fill(self.theta, self.data[i], color=colour_Bar[i], alpha=0.25)
            self.axes.set_rgrids(np.arange(20, 100, 20), labels=np.arange(20, 100, 20), angle=0)
            self.axes.set_thetagrids(self.theta * (180 / np.pi), labels=np.array(["A", "B", "C", "D", "E", "F"]))
            self.axes.set_title("Rating Comparison")
        self.axes.legend(self.legends)

    def plot_original_fig_sb(self, original_data):
        self.axes = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])

        time_data = original_data.time_data
        sr_x_data = original_data.sr_x_data
        sr_y_data = original_data.sr_y_data
        sr_z_data = original_data.sr_z_data

        self.axes.plot(time_data, sr_x_data, color='black')
        self.axes.plot(time_data, sr_y_data, color='red')
        self.axes.plot(time_data, sr_z_data, color='blue')
        exam_x = np.where(sr_x_data > 10)
        exam_y = np.where(sr_y_data > 10)
        exam_z = np.where(sr_z_data > 10)

        if exam_x[0].shape[0] > 0:
            for nn in exam_x:
                self.axes.plot(time_data[nn], sr_x_data[nn], color='red', marker='x', markersize=12)
                sr_x_data[nn] = 0
        if exam_y[0].shape[0] > 0:
            for nn in exam_y:
                self.axes.plot(time_data[nn], sr_y_data[nn], color='red', marker='x', markersize=12)
        if exam_z[0].shape[0] > 0:
            for nn in exam_z:
                self.axes.plot(time_data[nn], sr_z_data[nn], color='red', marker='x', markersize=12)

        self.axes.set_xlabel('Time (s)', fontsize=10)
        self.axes.set_ylabel('Acc (g)', fontsize=10)
        self.axes.set_title('Speed bump 20kph', fontsize=12)

    def plot_filter_fig_sb(self, filter_data):
        time_data = filter_data.time_data
        sr_x_filter = filter_data.sr_x_data
        sr_y_filter = filter_data.sr_y_data
        sr_z_filter = filter_data.sr_z_data
        self.axes.plot(time_data, sr_x_filter, color='black')
        self.axes.plot(time_data, sr_y_filter, color='red')
        self.axes.plot(time_data, sr_z_filter, color='blue')
        self.axes.set_xlabel('Time (s)', fontsize=10)
        self.axes.set_ylabel('Acc (g)', fontsize=10)
        self.axes.set_title('Speed bump 20kph', fontsize=14)

    def plot_result_keyonff(self, key_on_off_fig, original_data):
        # 作图，把计算得到的特征点标注在图中
        index_st = key_on_off_fig.index_st
        index_snd = key_on_off_fig.index_snd
        index_crank_st = key_on_off_fig.index_crank_st
        index_crank_snd = key_on_off_fig.index_crank_snd
        index_flare = key_on_off_fig.index_flare
        spd_flare = key_on_off_fig.spd_flare
        time_data = original_data.time_data
        spd_data = original_data.spd_data

        self.axes.set_title('Result of key on and off', fontsize=14)
        self.axes.set_xlabel('time', fontsize=12)
        self.axes.set_ylabel('eng_spd', fontsize=12)
        self.axes.plot(time_data, spd_data, color='blue', linewidth=2)

        offset_x = 1
        offset_y = 2
        for NN in range(len(index_st)):
            self.axes.plot(time_data[index_st[NN]], spd_data[index_st[NN]], color='red', marker='.', markersize=18,
                           linewidth=2)
            self.axes.text(time_data[index_st[NN]] + offset_x, spd_data[index_st[NN]] + offset_y, 'start')

            self.axes.plot(time_data[index_snd[NN]], spd_data[index_snd[NN]], color='red', marker='^', markersize=10,
                           linewidth=2)
            self.axes.text(time_data[index_snd[NN]] + offset_x, spd_data[index_snd[NN]] + offset_y, 'end')

            self.axes.plot(time_data[index_crank_st[NN]], spd_data[index_crank_st[NN]], color='b', marker='.',
                           markersize=18, linewidth=2)
            self.axes.text(time_data[index_crank_st[NN]] + offset_x, spd_data[index_crank_st[NN]] + offset_y, 'crank_start')

            self.axes.plot(time_data[index_crank_snd[NN]], spd_data[index_crank_snd[NN]], color='b', marker='^',
                           markersize=10, linewidth=2)
            self.axes.text(time_data[index_crank_snd[NN]] + offset_x, spd_data[index_crank_snd[NN]] + offset_y, 'crank_end')

            self.axes.plot(time_data[index_flare[NN]], spd_flare[NN], color='black', marker='.', markersize=18,
                           linewidth=2)
            self.axes.text(time_data[index_flare[NN]] + offset_x, spd_data[index_flare[NN]] + offset_y, 'flare')

    def reset_i(self):
        self.i = 0
