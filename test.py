# def read_file(file_path, encoding='utf-8'):
#     try:
#         with open(file_path, 'r', encoding=encoding) as file:
#             lines = file.readlines()
#             return lines
#     except FileNotFoundError:
#         print(f"File '{file_path}' not found.")
#         return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# def main():
#     file_path = 'Action.txt'  # Thay thế bằng đường dẫn tới file của bạn

#     lines = read_file(file_path)

#     if lines is not None:
#         print("Array content:")
#         array_content = [line.strip() for line in lines]
#         print(array_content)

# if __name__ == "__main__":
#     main()
