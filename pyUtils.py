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

