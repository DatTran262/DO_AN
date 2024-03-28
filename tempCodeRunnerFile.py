# Timetable chứa các hàng chứa giá trị cuối cùng cần lưu
# timetable = [[1, 2, 3, 4, 5], [1, 5, 7, 2], [1, 34, 45, 4],[1, 2, 3, 4, 5], [1, 5, 7, 2], [1, 34, 45, 4], [1, 2, 3, 4, 5], [1, 5, 7, 2], [1, 34, 45, 4]]

# # Đường dẫn đến file txt để lưu trữ giá trị
# file_path = "D:\\Workspace\\timeTable.txt"

# # Mở file txt để ghi dữ liệu
# with open(file_path, "w") as file:
#     # Ghi các giá trị cuối cùng của mỗi hàng từ timetable vào file
#     for row in timetable:
#         last_value = row[-1]  # Lấy giá trị cuối cùng của hàng
#         file.write(f"{last_value} ")