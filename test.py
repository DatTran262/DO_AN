line = "P_Lock_10_11"
lock_actions = []
parts = line.split("_")[2:]  # Bắt đầu từ index 2 để loại bỏ "P_Lock" và phần số đầu tiên
lock_actions.append(parts)
print(lock_actions)