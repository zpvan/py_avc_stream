
import pySliceHeader

class Slice():

    def __init__(self, rbsp, sps_dict, pps_dict, nal_dict):
        self.rbsp = rbsp
        # print("slice hex = " + self.rbsp.hex())
        self.active_sps = sps_dict
        self.active_pps = pps_dict
        self.nal_info = nal_dict

    def parse(self):
        print("slice parse begin")

        self.header = pySliceHeader.SliceHeader(self.rbsp, self.active_sps, self.active_pps, self.nal_info)
        self.header.parse()

        print("slice parse end")
        pass

    def print_info(self):
        self.header.print_info()
        pass