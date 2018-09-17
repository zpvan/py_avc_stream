import math


class StrBinArray():

    def __init__(self, binary):
        self.binary = binary
        self.r_idx = 0

def read_bits(payload, int_size):
    if int_size == 0:
        return 0

    str_bits = payload.binary[payload.r_idx: payload.r_idx + int_size]
    int_bits = int(str_bits, 2)
    payload.r_idx = payload.r_idx + int_size
    return int_bits

def read_ue(payload):
    leading_zero_bits = 0
    while read_bits(payload, 1) == 0:
        leading_zero_bits = leading_zero_bits + 1

    num_1 = 1
    temp = leading_zero_bits
    while temp > 0:
        num_1 = 2 * num_1
        temp = temp - 1

    num_2 = 1

    num_3 = read_bits(payload, leading_zero_bits)

    result = num_1 - num_2 + num_3

    return result

def read_se(payload):
    ue = read_ue(payload)
    
    if ue % 2 == 0:
        num_1 = -1
    else:
        num_1 = 1

    num_2 = math.ceil(ue / 2)

    result = num_1 * num_2

    return result

def more_rbsp_data(payload):
    last_1_idx = payload.binary.rfind("1")
    if payload.r_idx < last_1_idx:
        return True

    return False

def scaling_list(str_payload, scaling_list, size_of_scaling_list, use_default_scaling_matrix_flag):
        last_scale = 8
        next_scale = 8
        for j in range(size_of_scaling_list):
            if next_scale != 0:
                delta_scale = read_se(str_payload)
                next_scale = math.floor((last_scale + delta_scale + 256) % 256)
                use_default_scaling_matrix_flag = (j == 0 and next_scale == 0)
            if next_scale == 0:
                scaling_list[j] = last_scale
            else:
                scaling_list[j] = next_scale
            last_scale = scaling_list[j]

def rbsp_trailing_bits(str_payload):
    last_payload = str_payload.binary[str_payload.r_idx:]
    print("rbsp_trailing_bits() binary of last_payload = " + last_payload)

