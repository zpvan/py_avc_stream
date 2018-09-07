
import os

# huffman encode

def calu_file_size(file_name):
    print("file_size = " + str(os.path.getsize(file_name)) + " Byte")

def read_file_to_dict(file_name):
    dict_char = {}
    try:
        with open(file_name, "rb") as file_obj:
            content = file_obj.read()
            for char in content:
                if char in dict_char:
                    dict_char[char] = dict_char[char] + 1
                else:
                    dict_char[char] = 1  

    except FileNotFoundError:
        msg = "Sorry, " + file_name + " does not exits"
        print(msg)

    return dict_char

def sorted_dict(dict_char):
    # 对字典value进行排序
    return dict(sorted(dict_char.items(),key = lambda x:x[1],reverse = True))

def print_dict(dict_char):
    # 遍历sorted_dict_char
    for key, value in dict_char.items():
        print("[" + str(key) + ", " + str(value) + "]")


file_name = "logcat.log"

calu_file_size(file_name)

dict_char = read_file_to_dict(file_name)

dict_char = sorted_dict(dict_char)

print_dict(dict_char)

(key, value) = dict_char.popitem()
print("key,value = " + str(key) + ", " + str(value))

