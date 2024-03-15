# Lưu thông tin về các zip vào một tệp văn bản
def save_zip_info(zip_info, file_path):
    with open(file_path, 'w') as file:
        for zip_code, actions in zip_info.items():
            file.write(f'Zip {zip_code}:\n')
            for action in actions:
                file.write(f'- {action}\n')

# Đọc thông tin về các zip từ tệp văn bản và trả về dưới dạng một từ điển
def read_zip_info(file_path):
    zip_info = {}
    current_zip = None
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('Zip'):
                current_zip = line.split(':')[1].strip()
                zip_info[current_zip] = []
            elif line.strip():
                zip_info[current_zip].append(line.strip())
    return zip_info

# Dữ liệu cần lưu
zip_info = {
    '1001': ['Action 1', 'Action 2'],
    '1002': ['Action 3', 'Action 4'],
    '1003': ['Action 5', 'Action 6']
}

# Ghi thông tin về các zip vào tệp văn bản
file_path = 'Zip.txt'
save_zip_info(zip_info, file_path)

# Đọc thông tin về các zip từ tệp văn bản
read_zip_info = read_zip_info(file_path)

# In ra thông tin đọc được
for zip_code, actions in read_zip_info.items():
    print(f'Zip {zip_code}:')
    for action in actions:
        print(f'- {action}')
