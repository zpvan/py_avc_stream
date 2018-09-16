

# 264标准文档7章

# nalu type
# 7 => Sequence parameter set
# 8 => Pictrue parameter set
# 6 => Supplemental enhancement information
# 5 => Coded slice of an IDR picture
# 1 => Coded slice of a non-IDR piture
dict_nalu_type = {"sps" : 7, "pps" : 8, "sei" : 6, "i_frame" : 5, "p_frame" : 1}

# nalu body
# body => EBSP(RBSP(SODB)

class Nalu():

    def __init__(self, unit):
        self.unit = unit
        self.header = unit[0]
        self.body = unit[1:]
        self.rbsp = b''

    def parse(self):
        # parse header
        self.nal_ref_idc = (self.header & 0x60) >> 4
        self.nalu_unit_type = self.header & 0x1f

        # parse body
        body_part = self.body.partition(b'\x00\x00\x03')
        emulation_prevention_three_byte = body_part[1]
        while (len(emulation_prevention_three_byte) > 0) and (len(body_part[2]) > 0):
            self.body = body_part[0] + b'\x00\x00' + body_part[2]
            body_part = self.body.partition(b'\x00\x00\x03')
            emulation_prevention_three_byte = body_part[1]
        self.rbsp = body_part[0]


    def print_info(self):
        print("nalu info: ")
        print("nal_ref_idc = " + str(self.nal_ref_idc))
        print("nal_unit_type = " + str(self.nalu_unit_type))
        # print("nalu unit hex = " + str(self.unit.hex()))
