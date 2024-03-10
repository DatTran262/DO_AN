# import numpy as np

# class Robot:
#     def __init__(self):
#         self.timeTable = [[1, 2, 3], [4, 5], [6], [7, 8, 9, 10], [11, 12], [13, 14, 15], [16], [17, 18, 19], [11, 12], [13, 14, 15], [16], [17, 18, 19]]

#     def max_len_part(self, bodypart):
#         maxLen = 0
#         if bodypart == 'righthand':
#             for _row in range(9, 12):
#                 maxLen = max(maxLen, len(self.timeTable[_row]))
#         elif bodypart == 'body':
#             for _row in range(6):
#                 maxLen = max(maxLen, len(self.timeTable[_row]))
#         elif bodypart == 'lefthand':
#             for _row in range(6, 9):
#                 maxLen = max(maxLen, len(self.timeTable[_row]))
#         return maxLen

#     def check_lock_part(self, id):
#         lockPart = []
#         if 9 <= id <= 11: lockPart = [9, 10, 11]
#         elif 6 <= id <= 8: lockPart = [6, 7, 8]
#         elif 0 <= id <= 5: lockPart = [0, 1, 2, 3, 4, 5]
#         return lockPart

#     def lock_part(self, bodypart, id):
#         max_rowLen = self.max_len_part(bodypart)
#         lockkid = self.check_lock_part(id)
#         for i, v in enumerate(self.timeTable):
#             if i in lockkid and (len(v) < max_rowLen):
#                 last_value = v[-1]
#                 remain_time = max_rowLen - len(v)
#                 self.timeTable[i] = np.append(v, np.ones(remain_time) * last_value)

# robot = Robot()

# print("Before locking:")
# for i, row in enumerate(robot.timeTable):
#     print(f"Row {i}: {row}")

# # Lock lefthand (id 6-8)
# robot.lock_part('lefthand', 6)

# print("\nAfter locking lefthand:")
# for i, row in enumerate(robot.timeTable):
#     print(f"Row {i}: {row}")

# # Lock righthand (id 9-11)
# robot.lock_part('righthand', 9)

# print("\nAfter locking righthand:")
# for i, row in enumerate(robot.timeTable):
#     print(f"Row {i}: {row}")



import numpy as np

def giai_ma_tran(A, b):
    # Giải hệ phương trình tuyến tính Ax = b
    x = np.linalg.solve(A, b)
    return x

def rut_gon_ma_tran(A):
    # Rút gọn ma trận A
    A_reduced = np.around(A, decimals=2)
    return A_reduced

# Ví dụ về giải ma trận
A = np.array([[2, 1, -1],
              [-3, -1, 2],
              [-2, 1, 2]])
b = np.array([8, -11, -3])

x = giai_ma_tran(A, b)
print("Nghiệm của hệ phương trình:", x)

# Ví dụ về rút gọn ma trận
B = np.array([[1.235, 2.315, 3.445],
              [4.556, 5.675, 6.789],
              [7.123, 8.234, 9.345]])

B_reduced = rut_gon_ma_tran(B)
print("Ma trận sau khi rút gọn:")
print(B_reduced)