import numpy as np
from tf import HomogeneousMatrix
import math
from math import radians

class TimeTable:
    def __init__(self, totalRow, homePose):
        self.timeTable = list()

        self.originTable = list()
       
        try:
            assert len(homePose.jointValues) == totalRow
            for i in range(totalRow):
                self.timeTable.append(np.array((homePose.jointValues[i])).ravel())
                self.originTable.append(np.array((homePose.jointValues[i])).ravel())

        except:
            raise Exception("Time Table initialize error")

   
    def addAction(self, jointAct):
        if (jointAct.lockType == 'lock'):
            self.lock()
            self.moveJoint(id = jointAct.jointID, targetValue = jointAct.targetValue, speed = jointAct.speed)
            self.lock()
        elif (jointAct.lockType == 'union'):
            self.moveJoint(id = jointAct.jointID, targetValue = jointAct.targetValue, speed = jointAct.speed)        
        else:
            raise Exception("Unknown joint action")
       
    def addPose(self, poseAct):
        for i in range(len(poseAct.jointValues)):
            self.moveJoint(id = i, targetValue = poseAct.jointValues[i], speed = poseAct.jointSpeeds[i])
        self.lock()

    def gen_jointList(self):
        self.lock()
        return np.stack(self.timeTable).T
   
    def max_len(self):
        maxLen = 0
        for _row in self.timeTable:
            maxLen = max(maxLen, len(_row))
        return maxLen

    def lock(self):
        max_rowLen = self.max_len()
       
        for i, v in enumerate(self.timeTable):
            if (len(v) == max_rowLen): continue
            if (len(v) < max_rowLen):
                last_value = v[-1]
                remain_time = max_rowLen - len(v)
                self.timeTable[i] = np.append(v, np.ones(remain_time) * last_value)
   
    def moveJoint(self,id, targetValue, speed):
        lastValue = self.timeTable[id][-1]
        assert (speed > 0)
        if (lastValue > targetValue):
            temp = np.append(np.arange(lastValue, targetValue, -speed), [targetValue])
        else:
            temp = np.append(np.arange(lastValue, targetValue, speed), [targetValue])
       
        self.timeTable[id] = np.append(self.timeTable[id], np.delete(temp, 0))

    def reset(self):
        self.timeTable = self.originTable

    def prepare(self, listEvents):
        for i in listEvents:
            if (type(i) is JointAction):
                self.addAction(i)
            elif (type(i) is Pose):
                self.addPose(i)
            else: raise Exception("Time Table prepare error")

class JointAction:
    def __init__(self, name, jointID, lockType, targetValue, speed):
        self.jointID = jointID
        self.lockType = lockType
        self.targetValue = targetValue
        self.name = name
        self.speed = speed

class Pose:
    def __init__(self, name, jointValues, jointSpeeds):
        self.name = name
        self.jointValues = jointValues
        self.jointSpeeds = jointSpeeds

class _Robot():
    def __init__(self):
        self.numJoint = 3
        self.linkColour = ['red', 'yellow', 'black']
        self.jointType = ['r', 'r', 'r']

        self._linkColour = ['red', 'black', 'black', 'yellow']
        self._jointType = ['r', 'l']


        self.L = [0.56, 0.42, 0.24]

        self.Q = [0, 0.3, -0.25]

        self.limit = [ (-np.pi/2, np.pi/2) , (0, np.pi/2), (-np.pi/2, 0)]
        self.jointSpeeds = [ np.pi/6, np.pi/6, np.pi/6]
        self.poseJointSpeeds = self.jointSpeeds
        self.QHome = Pose('Home', self.Q.copy(), self.poseJointSpeeds.copy())

    def gen_jointSpeeds(self):
        for i in range(self.numJoint):
            self.poseJointSpeeds[i] = (self.limit[i][1] - self.limit[i][0]) / 10

    def set_jointHome(self, QPose):
        if not(QPose.name == 'Home'): return False
        self.QHome = QPose.copy()
        return True

    def check_limit(self):
        for i in range(self.numJoint):
            if (self.Q[i] > self.limit[i][1]) or (self.Q[i] < self.limit[i][0]): return False
        return True

    def check_limitId(self, jointId, jointValue):
        if (jointId < 0) or (jointId >= self.numJoint): return False
        if (jointValue > self.limit[jointId][1]) or (jointValue < self.limit[jointId][0]): return False
        return True

    def apply_value(self, jointConfig):
        if (len(jointConfig) != self.numJoint): return False
        for i in range(self.numJoint):
            self.Q[i] = jointConfig[i]
        return True

    def update_length(self, index, value):
        if (index >= numJoint): return False
        # for i in range(index):
        #     if (value > self.L[i]): return False
        self.L[index] = value
        if (self.jointType[index] == 'l'): self.limit[index][1] = value
        return True

    def update_limit(self, index, value_min, value_max):
        if (index >= numJoint): return False
        if (value_min > value_max): return False
        self.limit[index] = (value_min, value_max)
        self.gen_jointSpeeds()
        return True

    def gen_jointTrajectory(self, listActions):
        jointTrajectory = []
        dummy = listActions.copy()
        # convert all to config
        if dummy is None: return False
        if not(dummy[0][2] == '_Pose_'): dummy.append(0, self.QHome)
            
        # gen joint tracjectory with config
        pass

    def gen_jointSpace(self):
        self.jointSpace = np.mgrid[[slice(row[0], row[1], self.pointStep*1j) for row in self.limit]].reshape(self.numJoint,-1).T


class RobotUR5(_Robot):
    def __init__(self):
        super(RobotUR5, self).__init__()
        self.numJoint = 12
        self.linkColour = self._linkColour[:self.numJoint]
        self.jointType = ['l', 'l', 'r', 'r', 'r','r']
        self.jointArmTypeR = ['l', 'r', 'r']
        self.jointArmTypeL = ['l', 'r', 'r']

        self.L = [0.28, 0.17, 0.05, 0.17, -0.05, 0.05, 0.12, 0.08]

        self.Q = [0.5, 0.75, np.pi/2, np.pi/2, np.pi/2, np.pi/2, 0.05, np.pi/2, np.pi/2, -0.05, np.pi/2, np.pi/2]

        self.limit = [ (0, 1), (0, 1), (0, np.pi/2), (0, np.pi/2), (0, np.pi*5/6), (0, np.pi/2), 
                       (-1, 1), (-np.pi/2, 0), (-np.pi*5/6, np.pi*5/6), 
                       (-1, 1), (-np.pi/2, 0), (-np.pi*5/6, np.pi*5/6) ]

        self.jointSpeeds = [ 0.25, 0.25, np.pi/12, np.pi/12, np.pi/12, np.pi/12, 0.05, np.pi/12, np.pi/12, 0.05, np.pi/12, np.pi/12 ]
        self.poseJointSpeeds = self.jointSpeeds
        # self.gen_jointSpeeds()

        self.QHome = Pose('Home', self.Q.copy(), self.poseJointSpeeds.copy())

        #Define waypoint body
        self.waypointX = [0, 0, 0, 0, 0, 0]
        self.waypointY = [0, 0, 0, 0, 0, 0]
        self.waypointZ = [0, 0, 0, 0, 0, 0]
        #Define waaypoint arm right
        self.waypointRX = [0, 0, 0]
        self.waypointRY = [0, 0, 0]
        self.waypointRZ = [0, 0, 0]
        #Define waaypoint arm left
        self.waypointLX = [0, 0, 0]
        self.waypointLY = [0, 0, 0]
        self.waypointLZ = [0, 0, 0]

        self.jointSpace = []
        self.pointStep = 3
        self.gen_jointSpace()
        self.init_dh()
        self.get_waypoint()


    def init_dh(self):
        self.base = HomogeneousMatrix()
        self.joint1 = HomogeneousMatrix()
        self.joint2 = HomogeneousMatrix()
        self.joint3 = HomogeneousMatrix()
        self.joint4 = HomogeneousMatrix()
        self.joint5 = HomogeneousMatrix()
        self.joint6 = HomogeneousMatrix()
        self.joint7 = HomogeneousMatrix()
        self.joint8 = HomogeneousMatrix()
        self.joint9 = HomogeneousMatrix()
        self.joint10 = HomogeneousMatrix()
        self.joint11 = HomogeneousMatrix()


    def forward_kinematic(self):
        self.base.complete  (0        , 0        , self.Q[0], 0        )
        self.joint1.complete(0        , np.pi/2  , self.Q[1], 0        )
        self.joint2.complete(self.L[0], self.Q[2], 0        , self.Q[3])
        self.joint3.complete(self.L[1], self.Q[4], 0        , self.Q[4])
        self.joint4.complete(self.L[2], self.Q[5], 0        , 0        )

        # Join transfer
        self.joint5.complete(self.L[3], self.Q[4], 0        , self.Q[4])

        #Join arm right
        self.joint6.complete(0        , 0        , self.L[4], 0        )
        self.joint7.complete(self.L[6], self.Q[7], 0        , 0        )
        self.joint8.complete(self.L[7], self.Q[8], 0        , 0        )

        #Join arm right
        self.joint9.complete (0        , 0         , self.L[5], 0        )
        self.joint10.complete(self.L[6], self.Q[10], 0        , 0        )
        self.joint11.complete(self.L[7], self.Q[11], 0        , 0        )

        # ---------------------------------
        self.joint1.set_parent(self.base.get())
        self.joint2.set_parent(self.joint1.get())
        self.joint3.set_parent(self.joint2.get())
        self.joint4.set_parent(self.joint3.get())

        self.joint5.set_parent(self.joint2.get())

        self.joint6.set_parent(self.joint5.get())
        self.joint7.set_parent(self.joint6.get())
        self.joint8.set_parent(self.joint7.get())

        self.joint9.set_parent(self.joint5.get())
        self.joint10.set_parent(self.joint9.get())
        self.joint11.set_parent(self.joint10.get())


        #Set waypoint body
        self.waypointX = [self.base[0, 3], self.joint1[0, 3], self.joint2[0, 3], self.joint3[0, 3], self.joint4[0, 3]]
        self.waypointY = [self.base[1, 3], self.joint1[1, 3], self.joint2[1, 3], self.joint3[1, 3], self.joint4[1, 3]]
        self.waypointZ = [self.base[2, 3], self.joint1[2, 3], self.joint2[2, 3], self.joint3[2, 3], self.joint4[2, 3]]
        #Set waypoint arm right
        self.waypointRX = [self.joint5[0, 3], self.joint6[0, 3], self.joint7[0, 3], self.joint8[0, 3]]
        self.waypointRY = [self.joint5[1, 3], self.joint6[1, 3], self.joint7[1, 3], self.joint8[1, 3]]
        self.waypointRZ = [self.joint5[2, 3], self.joint6[2, 3], self.joint7[2, 3], self.joint8[2, 3]]
        #Set waypoint arm left
        self.waypointLX = [self.joint5[0, 3], self.joint9[0, 3], self.joint10[0, 3], self.joint11[0, 3]]
        self.waypointLY = [self.joint5[1, 3], self.joint9[1, 3], self.joint10[1, 3], self.joint11[1, 3]]
        self.waypointLZ = [self.joint5[2, 3], self.joint9[2, 3], self.joint10[2, 3], self.joint11[2, 3]]


    def get_waypoint(self):
        if not (self.check_limit()): return False
        self.forward_kinematic()
        return True