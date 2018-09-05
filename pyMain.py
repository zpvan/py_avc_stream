import pyAvcStream
import pyNalu
import pySps

file_name = "1920x1080x60x1sec-startWithSps.264"

# 解析流,提取出nalu的字节buf放到list_bytes_nalu列表里边
list_bytes_nalu = []
start_code = pyAvcStream.read_264_file_to_nalus(file_name, list_bytes_nalu)

print("nalu count = " + str(len(list_bytes_nalu)) + ", start_code = " + str(start_code))

# 解析nalu,将nalu放到nalus列表里边
nalus = []
for bytes_nalu in list_bytes_nalu:
    nalu = pyNalu.Nalu(bytes_nalu[len(start_code):])
    nalu.parse()
    nalus.append(nalu)

# 创建一个gop列表来存各种解析好了的数据
gop = []

for nalu in nalus:
    if nalu.nalu_unit_type == pyNalu.dict_nalu_type["sps"]:
        sps = pySps.Sps(nalu.rbsp)
        sps.parse()
        gop.append(sps)
    elif nalu.nalu_unit_type == pyNalu.dict_nalu_type["pps"]:
        pass
    elif nalu.nalu_unit_type == pyNalu.dict_nalu_type["sei"]:
        pass
    elif nalu.nalu_unit_type == pyNalu.dict_nalu_type["i_frame"]:
        pass
    elif nalu.nalu_unit_type == pyNalu.dict_nalu_type["p_frame"]:
        pass
    else:
        print("unknown nalu type DEC = " + nalu.nalu_unit_type)

print("gop count = " + str(len(gop)))
