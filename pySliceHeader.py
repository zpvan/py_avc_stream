import pyUtils
from bitstring import BitStream, BitArray
import pprint
from collections import OrderedDict

class SliceHeader():

    def __init__(self, rbsp, sps_dict, pps_dict, nal_dict):
        self.dict_info = OrderedDict()

        self.rbsp = rbsp
        self.active_sps = sps_dict
        self.active_pps = pps_dict
        self.nal_info = nal_dict

    def ref_pic_list_reordering(self, str_payload):
        dict_info = self.dict_info

        if (dict_info["slice_type"] % 5) != 2 and (dict_info["slice_type"] % 5) != 4:
            # slice_type != I and slice_type != SI
            dict_info["ref_pic_list_reordering_flag_l0"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["ref_pic_list_reordering_flag_l0"] == 1:
                dict_info["reordering_of_pic_nums_idc"] = 0
                while dict_info["reordering_of_pic_nums_idc"] != 3:
                    dict_info["reordering_of_pic_nums_idc"] = pyUtils.read_ue(str_payload)
                    if dict_info["reordering_of_pic_nums_idc"] == 0 or dict_info["reordering_of_pic_nums_idc"] == 1:
                        dict_info["abs_diff_pic_num_minus1"] = pyUtils.read_ue(str_payload)
                    elif dict_info["reordering_of_pic_nums_idc"] == 2:
                        dict_info["long_term_pic_num"] = pyUtils.read_ue(str_payload)

        if (dict_info["slice_type"] % 5) == 1:
            # slice_type == B
            dict_info["ref_pic_list_reordering_flag_l1"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["ref_pic_list_reordering_flag_l1"] == 1:
                dict_info["reordering_of_pic_nums_idc"] = 0
                while dict_info["reordering_of_pic_nums_idc"] != 3:
                    dict_info["reordering_of_pic_nums_idc"] = pyUtils.read_ue(str_payload)
                    if dict_info["reordering_of_pic_nums_idc"] == 0 or dict_info["reordering_of_pic_nums_idc"] == 1:
                        dict_info["abs_diff_pic_num_minus1"] = pyUtils.read_ue(str_payload)
                    elif dict_info["reordering_of_pic_nums_idc"] == 2:
                        dict_info["long_term_pic_num"] = pyUtils.read_ue(str_payload)

    def pred_weight_table(self, str_payload):
        dict_info = self.dict_info
        active_sps = self.active_sps

        dict_info["luma_log2_weight_denom"] = pyUtils.read_ue(str_payload)
        if active_sps["chroma_format_idc"] != 0:
            dict_info["chroma_log2_weight_denom"] = pyUtils.read_ue(str_payload)

        dict_info["luma_weight_l0"] = [0 for i in range(dict_info["num_ref_idx_l0_active_minus1"] + 1)]
        dict_info["luma_offset_l0"] = [0 for i in range(dict_info["num_ref_idx_l0_active_minus1"] + 1)]
        dict_info["chroma_weight_l0"] = [[0 for j in range(2)] for i in range(dict_info["num_ref_idx_l0_active_minus1"] + 1)]
        dict_info["chroma_offset_l0"] = [[0 for j in range(2)] for i in range(dict_info["num_ref_idx_l0_active_minus1"] + 1)]
        for i in range(dict_info["num_ref_idx_l0_active_minus1"] + 1):
            dict_info["luma_weight_l0_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["luma_weight_l0_flag"] == 1:
                dict_info["luma_weight_l0"][i] = pyUtils.read_se(str_payload)
                dict_info["luma_offset_l0"][i] = pyUtils.read_se(str_payload)
            if active_sps["chroma_format_idc"] != 0:
                dict_info["chroma_weight_l0_flag"] = pyUtils.read_bits(str_payload, 1)
                if dict_info["chroma_weight_l0_flag"] == 1:
                    for j in range(2):
                        dict_info["chroma_weight_l0"][i][j] = pyUtils.read_se(str_payload)
                        dict_info["chroma_offset_l0"][i][j] = pyUtils.read_se(str_payload)
        
        if (dict_info["slice_type"] % 5) == 1:
            # slice_type == B
            dict_info["luma_weight_l1"] = [0 for i in range(dict_info["num_ref_idx_l1_active_minus1"] + 1)]
            dict_info["luma_offset_l1"] = [0 for i in range(dict_info["num_ref_idx_l1_active_minus1"] + 1)]
            dict_info["chroma_weight_l1"] = [[0 for j in range(2)] for i in range(dict_info["num_ref_idx_l1_active_minus1"] + 1)]
            dict_info["chroma_offset_l1"] = [[0 for j in range(2)] for i in range(dict_info["num_ref_idx_l1_active_minus1"] + 1)]
            for i in range(dict_info["num_ref_idx_l1_active_minus1"] + 1):
                dict_info["luma_weight_l1_flag"] = pyUtils.read_bits(str_payload, 1)
                if dict_info["luma_weight_l1_flag"] == 1:
                    dict_info["luma_weight_l1"][i] = pyUtils.read_se(str_payload)
                    dict_info["luma_offset_l1"][i] = pyUtils.read_se(str_payload)
                if active_sps["chroma_format_idc"] != 0:
                    dict_info["chroma_weight_l1_flag"] = pyUtils.read_bits(str_payload, 1)
                    if dict_info["chroma_weight_l1_flag"] == 1:
                        for j in range(2):
                            dict_info["chroma_weight_l1"][i][j] = pyUtils.read_se(str_payload)
                            dict_info["chroma_offset_l1"][i][j] = pyUtils.read_se(str_payload)

    def dec_ref_pic_marking(self, str_payload):
        dict_info = self.dict_info
        nal_info = self.nal_info

        if nal_info["nal_unit_type"] == 5:
            dict_info["no_output_of_prior_pics_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["long_term_reference_flag"] = pyUtils.read_bits(str_payload, 1)
        else:
            dict_info["adaptive_ref_pic_marking_mode_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["adaptive_ref_pic_marking_mode_flag"] == 1:
                dict_info["memory_management_control_operation"] = 1
                while dict_info["memory_management_control_operation"] != 0:
                    dict_info["memory_management_control_operation"] = pyUtils.read_ue(str_payload)
                    if dict_info["memory_management_control_operation"] == 1 or dict_info["memory_management_control_operation"] == 3:
                        dict_info["difference_of_pic_nums_minus1"] = pyUtils.read_ue(str_payload)
                    if dict_info["memory_management_control_operation"] == 2:
                        dict_info["long_term_pic_num"] = pyUtils.read_ue(str_payload)
                    if dict_info["memory_management_control_operation"] == 3 or dict_info["memory_management_control_operation"] == 6:
                        dict_info["long_term_frame_idx"] = pyUtils.read_ue(str_payload)
                    if dict_info["memory_management_control_operation"] == 4:
                        dict_info["max_long_term_frame_idx_plus1"] = pyUtils.read_ue(str_payload)

    def parse(self):
        print("slice_header parse begin")
        dict_info = self.dict_info
        active_sps = self.active_sps
        active_pps = self.active_pps
        nal_info = self.nal_info

        str_slice_header_bin = BitArray(self.rbsp).bin
        # print("slice header binary = " + str_slice_header_bin)
        str_payload = pyUtils.StrBinArray(str_slice_header_bin)

        dict_info["first_mb_in_slice"] = pyUtils.read_ue(str_payload)
        dict_info["slice_type"] = pyUtils.read_ue(str_payload)
        dict_info["pic_parameter_set_id"] = pyUtils.read_ue(str_payload)
        dict_info["frame_num"] = pyUtils.read_bits(str_payload, active_sps["log2_max_frame_num_minus4"] + 4)
        if active_sps["frame_mbs_only_flag"] == 0:
            dict_info["field_pic_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["field_pic_flag"] == 1:
                dict_info["bottom_field_flag"] = pyUtils.read_bits(str_payload, 1)
        if nal_info["nal_unit_type"] == 5:
            dict_info["idr_pic_id"] = pyUtils.read_ue(str_payload)
        if active_sps["pic_order_cnt_type"] == 0:
            dict_info["pic_order_cnt_lsb"] = pyUtils.read_bits(str_payload, active_sps["log2_max_pic_order_cnt_lsb_minus4"] + 4)
            if active_pps["pic_order_present_flag"] == 1 and dict_info["field_pic_flag"] == 0:
                dict_info["delta_pic_order_cnt_bottom"] = pyUtils.read_se(str_payload)
        if active_sps["pic_order_cnt_type"] == 1 and active_sps["delta_pic_order_always_zero_flag"] == 0:
            dict_info["delta_pic_order_cnt"] = []
            dict_info["delta_pic_order_cnt"].append(pyUtils.read_se(str_payload))
            if active_pps["pic_order_present_flag"] == 1 and dict_info["field_pic_flag"] == 0:
                dict_info["delta_pic_order_cnt"].append(pyUtils.read_se(str_payload))
        if active_pps["redundant_pic_cnt_present_flag"] == 1:
            dict_info["redundant_pic_cnt"] = pyUtils.read_ue(str_payload)
        if (dict_info["slice_type"] % 5) == 1:
            # slice_type == B
            dict_info["direct_spatial_mv_pred_flag"] = pyUtils.read_bits(str_payload, 1)
        if (dict_info["slice_type"] % 5) == 0 or (dict_info["slice_type"] % 5) == 3 or (dict_info["slice_type"] % 5) == 1:
            # slice_type == P or slice_type == SP or slice_type == B
            dict_info["num_ref_idx_active_override_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["num_ref_idx_active_override_flag"] == 1:
                dict_info["num_ref_idx_l0_active_minus1"] = pyUtils.read_ue(str_payload)
                if (dict_info["slice_type"] % 5) == 1:
                    dict_info["num_ref_idx_l1_active_minus1"] = pyUtils.read_ue(str_payload)
        self.ref_pic_list_reordering(str_payload)
        if (active_pps["weighted_pred_flag"] == 1 and ((dict_info["slice_type"] % 5) == 0 or (dict_info["slice_type"] % 5) == 3)) or (active_pps["weighted_bipred_idc"] == 1 and (dict_info["slice_type"] % 5) == 1):
            self.pred_weight_table(str_payload)
        if nal_info["nal_ref_idc"] != 0:
            self.dec_ref_pic_marking(str_payload)
        if active_pps["entropy_coding_mode_flag"] == 1 and (dict_info["slice_type"] % 5) != 2 and (dict_info["slice_type"] % 5) != 4:
            dict_info["cabac_init_idc"] = pyUtils.read_ue(str_payload)
        dict_info["slice_qp_delta"] = pyUtils.read_se(str_payload)
        if (dict_info["slice_type"] % 5) == 3 or (dict_info["slice_type"] % 5) == 4:
            if (dict_info["slice_type"] % 5) == 3:
                dict_info["sp_for_switch_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["slice_qs_delta"] = pyUtils.read_se(str_payload)
        if active_pps["deblocking_filter_control_present_flag"] == 1:
            dict_info["disable_deblocking_filter_idc"] = pyUtils.read_ue(str_payload)
            if dict_info["disable_deblocking_filter_idc"] != 1:
                dict_info["slice_alpha_c0_offset_div2"] = pyUtils.read_se(str_payload)
                dict_info["slice_beta_offset_div2"] = pyUtils.read_se(str_payload)
        if active_pps["num_slice_groups_minus1"] > 0 and active_pps["slice_group_map_type"] >= 3 and active_pps["slice_group_map_type"] <= 5:
            # self.slice_group_change_cycle = 
            pass

        print("slice_header parse begin")
        pass

    def print_info(self):
        print("slice header info:")
        pprint.pprint(self.dict_info)