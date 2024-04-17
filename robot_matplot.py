from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d, Axes3D 
from time import sleep
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import robot_class
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class DrawWidget(QtWidgets.QWidget):
    plot_done = pyqtSignal()
    plot_once = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.fig = Figure(dpi = 100)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.canvas.show()
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.axes.set_zlim3d(-0.2, 1)                    # viewrange for z-axis should be [-4,4] 
        self.axes.set_ylim3d(-1, 1)                    # viewrange for y-axis should be [-2,2] 
        self.axes.set_xlim3d(-1, 1)
        # self.axes.legend()
        self.current_point = []
        self.history_point = []

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(2) #time step

        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)

        self.jointTrajectory = []

        self.t_counter = 0

        self.robot = robot_class.RobotUR5()

        self.List_Pose = dict()
        self.List_Pose['Home'] = self.robot.QHome

        self.show()
    
    def reset(self):
        self.clear_pose()
        self.jointTrajectory = []
        self.refix(0)
        for line in self.axes.get_lines(): # ax.lines:
            line.remove()
        self.history_point = []
        self.canvas.draw()

    def change_robot(self, new_robot):
        self.robot = new_robot
        self.reset()

    def clear_pose(self):
        self.List_Pose = dict()
        self.List_Pose['Home'] = self.robot.QHome

    def setJointTrajectory(self, jointTrajectory):
        if (jointTrajectory is None): 
            print('none')
            self.jointTrajectory = self.robot.jointSpace
        else: 
            print('no none')
            self.jointTrajectory = jointTrajectory

    def robot_limit_plot(self):

        self.t_counter = 0
        if (len(self.jointTrajectory) == 0): self.setJointTrajectory(self.robot.jointSpace)
        self.history_point = []

        try:
            self.timer.timeout.disconnect()
        except:
            pass
        self.timer.timeout.connect(self.all_plot)
        self.timer.start()

    def plot_pause(self):
        self.timer.stop()
        try:
            self.timer.timeout.disconnect()
        except:
            pass
        self.refix(0)
        self.history_point = []

    def all_plot(self):
        file = "D:\\Workspace\\timeTable.txt"

        print("COUNTER NOW ", self.t_counter, " and total step ", len(self.jointTrajectory))
        if (self.t_counter >= len(self.jointTrajectory)):
            self.drawCurve()
            self.plot_pause()
            # output some signal to host to revert back button
            self.plot_done.emit()
            return

        self.robot.apply_value(self.jointTrajectory[self.t_counter])
        # print("self.jointTrajectory[self.t_counter]:", self.jointTrajectory[self.t_counter])
        with open(file, "w") as f:
            for row in self.jointTrajectory[self.t_counter]:
                f.write(f"{row} ")
        # print("APPLY VALUE ", self.robot.Q)

        self.plot()
        # self.robot.Q[0] = np.random.random()*(self.robot.limit[0][1] - self.robot.limit[0][0]) + self.robot.limit[0][0]
        self.t_counter += 1

    def drawCurve(self):
        temp_array = np.array(self.history_point).T
        self.axes.plot(temp_array[0], temp_array[1], color = 'brown')  
        self.canvas.draw()

    def refix(self, trim_len = 10):
        while (len(self.current_point) > trim_len): 
            last_point = self.current_point.pop(0)
            last_point.remove()

    def plot(self):
 
        for line in self.axes.get_lines(): # ax.lines:
            line.remove()

        self.robot.get_waypoint()
        for i in range(len(self.robot.waypointX) - 1):
            if i == 0:
                continue  # Đặt màu cho waypoint đầu tiên là màu đen
            else:
                self.axes.plot([self.robot.waypointX[i], self.robot.waypointX[i+1] ] , [self.robot.waypointY[i], self.robot.waypointY[i+1] ],\
                    '*--', color = self.robot.linkColour[i], zs= [self.robot.waypointZ[i], self.robot.waypointZ[i+1] ], label=str('Link ' + str(i))) 
        for i in range(len(self.robot.waypointRX) - 1):
            self.axes.plot([self.robot.waypointRX[i], self.robot.waypointRX[i+1] ] , [self.robot.waypointRY[i], self.robot.waypointRY[i+1] ],\
                '*--', color = self.robot.linkColour[1], zs= [self.robot.waypointRZ[i], self.robot.waypointRZ[i+1] ], label=str('Link ' + str(i)))
        for i in range(len(self.robot.waypointLX) - 1):
            self.axes.plot([self.robot.waypointLX[i], self.robot.waypointLX[i+1] ] , [self.robot.waypointLY[i], self.robot.waypointLY[i+1] ],\
                '*--', color = self.robot.linkColour[1], zs= [self.robot.waypointLZ[i], self.robot.waypointLZ[i+1] ], label=str('Link ' + str(i))) 
                
        self.history_point.append((self.robot.waypointX[1], self.robot.waypointY[1]))

        self.plot_once.emit()

        # self.refix()

        self.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = DrawWidget()
    app.exec()
