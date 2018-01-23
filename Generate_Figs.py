
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
            self.axes = self.fig.add_subplot(111)
        elif plot_type == '3d':
            self.axes = self.fig.add_subplot(111, projection='3d')
        elif plot_type == '2d-poly':
            self.axes = self.fig.add_subplot(111, polar=True)
        elif plot_type == '2d-multi':
            self.i = 0

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

        pos = [0.1, 0.1, 0.6, 0.8]
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
        self.axes.spines['right'].set_position(('outward', 60 * self.i))   # 图的右侧边框向外移动
        self.axes.spines['right'].set_color(colors[self.i])
        self.axes.spines['right'].set_linewidth(2)
        self.axes.plot(self.time, self.raw_data, linewidth=1, color=colors[self.i])
        self.axes.yaxis.set_ticks_position('right')
        self.axes.tick_params(axis='y', colors=colors[self.i])
        self.axes.set_ylabel(kwargs['legend'], fontsize=font_size, color=colors[self.i])
        self.axes.yaxis.set_label_position("right")
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


