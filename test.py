def replace_first_word_in_file(file_path, key_word, target_word, new_word):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            words = line.split()
            if key_word in words:  # Kiểm tra xem key_word có trong dòng không
                for i, word in enumerate(words):
                    if word == target_word:
                        words[i] = new_word
                        break
                line = ' '.join(words) + '\n'
            file.write(line)

# Sử dụng hàm replace_first_word_in_file để thay đổi từ đầu tiên trong mỗi dòng của tệp
file_path = 'Action.txt'
key_word = 'HR_wave_1'
target_word = '11'
new_word = '10'
replace_first_word_in_file(file_path, key_word, target_word, new_word)
