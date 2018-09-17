from bitstring import BitStream, BitArray
import pyUtils
import pprint
from collections import OrderedDict

class Pps():

    def __init__(self, rbsp):
        self.dict_info = OrderedDict()

        self.rbsp = rbsp
        print("pps hex = " + self.rbsp.hex())

    def parse(self):
        dict_info = self.dict_info

        str_pps_bin = BitArray(self.rbsp).bin
        print("pps binary = " + str_pps_bin)
        str_payload = pyUtils.StrBinArray(str_pps_bin)

        dict_info["pic_parameter_set_id"] = pyUtils.read_ue(str_payload)
        dict_info["seq_parameter_set_id"] = pyUtils.read_ue(str_payload)
        dict_info["entropy_coding_mode_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["pic_order_present_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["num_slice_groups_minus1"] = pyUtils.read_ue(str_payload)
        if dict_info["num_slice_groups_minus1"] > 0:
            dict_info["slice_group_map_type"] = pyUtils.read_ue(str_payload)
            if dict_info["slice_group_map_type"] == 0:
                dict_info["run_length_minus1"] = [0 for i in range(dict_info["num_slice_groups_minus1"] + 1)]
                for i_group in range(dict_info["num_slice_groups_minus1"] + 1):
                    dict_info["run_length_minus1"][i_group] = pyUtils.read_ue(str_payload)
            elif dict_info["slice_group_map_type"] == 2:
                dict_info["top_left"] = [0 for i in range(dict_info["num_slice_groups_minus1"] + 1)]
                dict_info["bottom_right"] = [0 for i in range(dict_info["num_slice_groups_minus1"] + 1)]
                for i_group in range(dict_info["num_slice_groups_minus1"] + 1):
                    dict_info["top_left"][i_group] = pyUtils.read_ue(str_payload)
                    dict_info["bottom_right"][i_group] = pyUtils.read_ue(str_payload)
            elif dict_info["slice_group_map_type"] == 3 or dict_info["slice_group_map_type"] == 4 or dict_info["slice_group_map_type"] == 5:
                dict_info["slice_group_change_direction_flag"] = pyUtils.read_bits(str_payload, 1)
                dict_info["slice_group_change_rate_minus1"] = pyUtils.read_ue(str_payload)
                dict_info["pic_size_in_map_units_minus1"] = pyUtils.read_ue(str_payload)
                for i in range(dict_info["pic_size_in_map_units_minus1"] + 1):
                    pass
        dict_info["num_ref_idx_l0_active_minus1"] = pyUtils.read_ue(str_payload)
        dict_info["num_ref_idx_l1_active_minus1"] = pyUtils.read_ue(str_payload)
        dict_info["weighted_pred_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["weighted_bipred_idc"] = pyUtils.read_bits(str_payload, 2)
        dict_info["pic_init_qp_minus26"] = pyUtils.read_se(str_payload)
        dict_info["pic_init_qs_minus26"] = pyUtils.read_se(str_payload)
        dict_info["chroma_qp_index_offset"] = pyUtils.read_se(str_payload)
        dict_info["deblocking_filter_control_present_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["constrained_intra_pred_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["redundant_pic_cnt_present_flag"] = pyUtils.read_bits(str_payload, 1)
        if pyUtils.more_rbsp_data(str_payload):
            dict_info["transform_8x8_mode_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["pic_scaling_matrix_present_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["pic_scaling_matrix_present_flag"] == 1:
                dict_info["pic_scaling_list_present_flag"] = [0 for i in range(6 + 2 * self.transform_8x8_mode_flag)]
                dict_info["scaling_list_4x4"] = [[0 for j in range(16)] for i in range(6)]
                dict_info["use_default_scaling_matrix_4x4_flag"] = [0 for i in range(6)]
                dict_info["scaling_list_8x8"] = [[0 for j in range(64)] for i in range(2)]
                dict_info["use_default_scaling_matrix_8x8_flag"] = [0 for i in range(2)]
                for i in range(6 + 2 * self.transform_8x8_mode_flag):
                    dict_info["pic_scaling_list_present_flag"][i] = pyUtils.read_bits(str_payload, 1)
                    if dict_info["pic_scaling_list_present_flag"][i] == 1:
                        if i < 6:
                            pyUtils.scaling_list(str_payload, dict_info["scaling_list_4x4"][i], 16, dict_info["use_default_scaling_matrix_4x4_flag"][i])
                        else:
                            pyUtils.scaling_list(str_payload, dict_info["scaling_list_8x8"][i - 6], 64, dict_info["use_default_scaling_matrix_8x8_flag"][i - 6])
            dict_info["second_chroma_qp_index_offset"] = pyUtils.read_se(str_payload)
            pyUtils.rbsp_trailing_bits(str_payload)
                
        # print("str_payload cur r_idx = " + str(str_payload.r_idx) + ", next bit = " + str(pyUtils.read_bits(str_payload, 1)))

    def print_info(self):
        print("pps info:")
        pprint.pprint(self.dict_info)