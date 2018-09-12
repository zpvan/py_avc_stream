# https://pythonhosted.org/bitstring/creation.html
# pip3.6.exe install bitstring // for windows
from bitstring import BitStream, BitArray

class Sps():

    def __init__(self, rbsp):
        self.rbsp = rbsp
        print("sps hex = " + self.rbsp.hex())
        

    def parse(self):
        print("sps parse begin")
        
        str_sps_bin = BitArray(self.rbsp).bin
        
        print("sps binary = " + str_sps_bin)

        print("sps parse end")


    def print_info(self):
        print("sps info: ")
