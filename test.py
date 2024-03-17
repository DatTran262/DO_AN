namePart = "P_Lock 8 9 10"

# Tách chuỗi thành các phần tử
parts = namePart.split()

# Tạo chuỗi mới bằng cách nối các phần tử với nhau, sử dụng dấu gạch dưới (_) thay vì khoảng trắng
new_name = parts[0] + "_" + "_".join(parts[1:])

print(new_name)