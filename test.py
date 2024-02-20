# def find_text_in_file(file_path, target_text):
#     try:
#         with open(file_path, 'r') as file:
#             for line in file:
#                 if target_text in line:
#                     return line.strip()  # Trả về dòng chứa target_text (loại bỏ ký tự xuống dòng)
#     except FileNotFoundError:
#         print(f"File '{file_path}' không tồn tại.")

# # Khởi tạo listactionName là một set rỗng
# listactionName = set()

# # Khởi tạo listAction là một dict rỗng
# listAction = {}

# # Đường dẫn đến file text
# file_path = "Action.txt"

# # Mở file text để đọc
# with open(file_path, 'r') as file:
#     # Đọc dòng đầu tiên từ file và thêm vào set listactionName
#     action_name = file.readline().strip()
#     listactionName.add(action_name)
    
#     # Đọc dòng thứ hai từ file và tách thành các phần tử
#     action_data = file.readline().strip().split()
    
#     # Lưu thông tin từ dòng thứ hai vào listAction dưới dạng key-value pairs
#     listAction[action_name] = {
#         "initial_angle": int(action_data[0]),
#         "joint_type": action_data[1],
#         "target_angle": int(action_data[2]),
#         "angular_speed": int(action_data[3])
#     }

# # In ra hai đối tượng listactionName và listAction
# print("List of action names:", listactionName)
# print("List of actions:", listAction)

# # Tìm kiếm giá trị trong file văn bản
# target_text = "HL"
# result = find_text_in_file(file_path, target_text)
# if result:
#     print("Dòng chứa giá trị cần tìm là:", result)
# else:
#     print("Không tìm thấy giá trị cần tìm trong file.")




# Đường dẫn đến file text
file_path = "Action.txt"

# Khởi tạo một dict để lưu các giá trị
values_dict = {}

# Mở file text để đọc
with open(file_path, 'r') as file:
    # Đọc từng dòng trong file
    for line in file:
        # Kiểm tra nếu dòng không rỗng
        if line.strip():
            # Tách từ đầu tiên từ dòng
            first_word, *other_values = line.strip().split()
            print('other_values[0]:', other_values[0])
            print('other_values[1]:', other_values[1])
            print('other_values[2]:', other_values[2])
            print('other_values[3]:', other_values[3])
            
            # Lưu các giá trị còn lại vào biến kiểu dict với từ đầu tiên làm key
            values_dict[first_word] = other_values

# In ra dict chứa các giá trị
print("Dict chứa các giá trị:", values_dict)

