import pyAvcStream
import pySps

file_name = "1920x1080x60x1sec-startWithSps.264"

# 解析流,提取出nalu放到nalus列表里边
nalus = []
start_code = pyAvcStream.read_264_file_to_nalus(file_name, nalus)

print("nalu count = " + str(len(nalus)) + ", start_code = " + str(start_code))

# 解析每种nalu
sps_byte = b'\x67'
pps_byte = b'\x68'
sei_byte = b'\x06'
i_frame_byte = b'\x65'
p_frame_byte = b'\x61'

# 创建一个gop列表来存各种解析好了的数据
gop = []

for nalu in nalus:
    if nalu.startswith(sps_byte, len(start_code)):
        sps = pySps.Sps(nalu)
        sps.parse()
        gop.append(sps)
    elif nalu.startswith(pps_byte, len(start_code)):
        print("pps hex = " + nalu.hex())
    elif nalu.startswith(sei_byte, len(start_code)):
        print("sei hex = " + nalu.hex())
    elif nalu.startswith(i_frame_byte, len(start_code)):
        pass
    elif nalu.startswith(p_frame_byte, len(start_code)):
        pass
    else:
        print("unknown nalu type DEC = " + nalu[len(start_code)])

print("gop count = " + str(len(gop)))
