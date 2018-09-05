import datetime

buf_size = 1024

three_start_code = b'\x00\x00\x01'
four_start_code = b'\x00\x00\x00\x01'

def find_start_code(buf):
    if buf.startswith(three_start_code):
        return three_start_code
    if buf.startswith(four_start_code):
        return four_start_code
    return b''


def separate_nalu(buf_prefix, buf, start_code, buf_list):
    while len(buf) > 0:
        buf_part = buf.partition(start_code)
        buf_prefix = buf_prefix + buf_part[0]
        if len(buf_part[1]) > 0:
            buf_list.append(buf_prefix)
            buf_prefix = buf_part[1]
            buf = buf_part[2]
        else :
            buf = b''
    return buf_prefix

def read_264_file_to_nalus(file_name, payloads):
    try:
        with open(file_name, "rb") as file_obj:
            buf = file_obj.read(4)
            start_code = find_start_code(buf)
            
            # 如果没有找到start_code就退出
            if start_code == b'':
                print("can't find start code, " + buf.hex())
                exit()

            # 开始计算耗时
            now = datetime.datetime.now().microsecond / 1000
            
            buf_prefix = buf
            buf = file_obj.read(buf_size)

            while len(buf) > 0:
                buf_prefix = separate_nalu(buf_prefix, buf, start_code, payloads)
                buf = file_obj.read(buf_size)

            payloads.append(buf_prefix)
            
            # print("payloads count = " + str(len(payloads)))
            # for payload in payloads:
            #     print("payload = " + payload[0:6].hex() + " size = " + str(len(payload)))

            # In range(1000000).
            cost = int(datetime.datetime.now().microsecond / 1000 - now)
            if cost < 0:
                cost = cost + 1000
                
            # print("cost " + str(cost) + " ms")
            
    except FileNotFoundError:
        msg = "Sorry, " + file_name + " does not exits."
        print(msg)

    return start_code
