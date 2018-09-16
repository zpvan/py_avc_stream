
import pySliceHeader

class Slice():

    def __init__(self, rbsp, sps, pps, nalu_type, nal_ref_idc):
        self.rbsp = rbsp
        # print("slice hex = " + self.rbsp.hex())
        self.sps = sps
        self.pps = pps
        self.nalu_type = nalu_type
        self.nal_ref_idc = nal_ref_idc

    def parse(self):
        print("slice parse begin")

        self.header = pySliceHeader.SliceHeader(self.rbsp, self.sps, self.pps, self.nalu_type, self.nal_ref_idc)
        self.header.parse()

        print("slice parse end")
        pass

    def print_info(self):
        self.header.print_info()
        pass