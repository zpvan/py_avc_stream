# https://pythonhosted.org/bitstring/creation.html
# pip3.6.exe install bitstring // for windows
# pip3 install bitstring // for mac
from bitstring import BitStream, BitArray
import pyUtils 
import math
import pprint
from collections import OrderedDict

class Sps():

    def __init__(self, rbsp):
        self.dict_info = OrderedDict()
        self.Extended_SAR = 255

        self.rbsp = rbsp
        print("sps hex = " + self.rbsp.hex())

    def hrd_parameters(self, str_payload):
        dict_info = self.dict_info

        dict_info["cpb_cnt_minus1"] = pyUtils.read_ue(str_payload)
        dict_info["bit_rate_scale"] = pyUtils.read_bits(str_payload, 4)
        dict_info["cpb_size_scale"] = pyUtils.read_bits(str_payload, 4)

        dict_info["bit_rate_value_minus1"] = [0 for i in range(dict_info["cpb_cnt_minus1"] + 1)]
        dict_info["cpb_size_value_minus1"] = [0 for i in range(dict_info["cpb_cnt_minus1"] + 1)]
        dict_info["cbr_flag"] = [0 for i in range(dict_info["cpb_cnt_minus1"] + 1)]
        for schedse1idex in range(dict_info["cpb_cnt_minus1"] + 1):
            dict_info["bit_rate_value_minus1"][schedse1idex] = pyUtils.read_ue(str_payload)
            dict_info["cpb_size_value_minus1"][schedse1idex] = pyUtils.read_ue(str_payload)
            dict_info["cbr_flag"][schedse1idex] = pyUtils.read_bits(str_payload, 1)
        
        dict_info["initial_cpb_removal_delay_length_minus1"] = pyUtils.read_bits(str_payload, 5)
        dict_info["cpb_removal_delay_length_minus1"] = pyUtils.read_bits(str_payload, 5)
        dict_info["dpb_output_delay_length_minus1"] = pyUtils.read_bits(str_payload, 5)
        dict_info["time_offset_length"] = pyUtils.read_bits(str_payload, 5)

    def vui_parameters(self, str_payload):
        dict_info = self.dict_info

        dict_info["aspect_ratio_info_present_flag"] = pyUtils.read_bits(str_payload, 1)
        if dict_info["aspect_ratio_info_present_flag"] == 1:
            dict_info["aspect_ratio_idc"] = pyUtils.read_bits(str_payload, 8)
            if dict_info["aspect_ratio_idc"] == self.Extended_SAR:
                dict_info["sar_width"] = pyUtils.read_bits(str_payload, 16)
                dict_info["sar_height"] = pyUtils.read_bits(str_payload, 16)
        dict_info["overscan_info_present_flag"] = pyUtils.read_bits(str_payload, 1)
        if dict_info["overscan_info_present_flag"] == 1:
            dict_info["overscan_appropriate_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["video_signal_type_present_flag"] = pyUtils.read_bits(str_payload, 1)
        if dict_info["video_signal_type_present_flag"] == 1:
            dict_info["video_format"] = pyUtils.read_bits(str_payload, 3)
            dict_info["video_full_range_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["colour_description_present_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["colour_description_present_flag"] == 1:
                dict_info["colour_primaries"] = pyUtils.read_bits(str_payload, 8)
                dict_info["transfer_characteristics"] = pyUtils.read_bits(str_payload, 8)
                dict_info["matrix_coefficients"] = pyUtils.read_bits(str_payload, 8)
        dict_info["chroma_loc_info_present_flag"] = pyUtils.read_bits(str_payload, 1)
        if dict_info["chroma_loc_info_present_flag"] == 1:
            dict_info["chroma_sample_loc_type_top_field"] = pyUtils.read_ue(str_payload)
            dict_info["chroma_sample_loc_type_bottom_field"] = pyUtils.read_ue(str_payload)
        dict_info["timing_info_present_flag"] = pyUtils.read_bits(str_payload, 1)
        if dict_info["timing_info_present_flag"] == 1:
            dict_info["num_units_in_tick"] = pyUtils.read_bits(str_payload, 32)
            dict_info["time_scale"] = pyUtils.read_bits(str_payload, 32)
            dict_info["fixed_frame_rate_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["nal_hrd_parameters_present_flag"] = pyUtils.read_bits(str_payload, 1)
        if dict_info["nal_hrd_parameters_present_flag"] == 1:
            self.hrd_parameters(str_payload)
        dict_info["vcl_hrd_parameters_present_flag"] = pyUtils.read_bits(str_payload, 1)
        if dict_info["vcl_hrd_parameters_present_flag"] == 1:
            self.hrd_parameters(str_payload)
        if dict_info["nal_hrd_parameters_present_flag"] == 1 or dict_info["vcl_hrd_parameters_present_flag"] == 1:
            dict_info["low_delay_hrd_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["pic_struct_present_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["bitstream_restriction_flag"] = pyUtils.read_bits(str_payload, 1)
        if dict_info["bitstream_restriction_flag"] == 1:
            dict_info["motion_vectors_over_pic_boundaries_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["max_bytes_per_pic_denom"] = pyUtils.read_ue(str_payload)
            dict_info["max_bits_per_mb_denom"] = pyUtils.read_ue(str_payload)
            dict_info["log2_max_mv_length_horizontal"] = pyUtils.read_ue(str_payload)
            dict_info["log2_max_mv_length_vertical"] = pyUtils.read_ue(str_payload)
            dict_info["num_reorder_frames"] = pyUtils.read_ue(str_payload)
            dict_info["max_dec_frame_buffering"] = pyUtils.read_ue(str_payload)

    def parse(self):
        dict_info = self.dict_info

        str_sps_bin = BitArray(self.rbsp).bin
        print("sps binary = " + str_sps_bin)
        str_payload = pyUtils.StrBinArray(str_sps_bin)

        dict_info["profile_idc"] = pyUtils.read_bits(str_payload, 8)
        dict_info["constraint_set0_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["constraint_set1_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["constraint_set2_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["constraint_set3_flag"] = pyUtils.read_bits(str_payload, 1)
        dict_info["reserved_zero_4bits"] = pyUtils.read_bits(str_payload, 4)
        dict_info["level_idc"] = pyUtils.read_bits(str_payload, 8)
        dict_info["seq_parameter_set_id"] = pyUtils.read_ue(str_payload)
        if (dict_info["profile_idc"] == 100 or dict_info["profile_idc"] == 110 or dict_info["profile_idc"] == 122 or dict_info["profile_idc"] == 144):
            dict_info["chroma_format_idc"] = pyUtils.read_ue(str_payload)
            if dict_info["chroma_format_idc"] == 3:
                dict_info["residual_colour_transform_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["bit_depth_luma_minus8"] = pyUtils.read_ue(str_payload)
            dict_info["bit_depth_chroma_minus8"] = pyUtils.read_ue(str_payload)
            dict_info["qpprime_y_zero_transform_bypass_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["seq_scaling_matrix_present_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["seq_scaling_matrix_present_flag"] == 1:
                dict_info["seq_scaling_list_present_flag"] = [0 for i in range(8)]
                dict_info["scaling_list_4x4"] = [[0 for j in range(16)] for i in range(6)]
                dict_info["use_default_scaling_matrix_4x4_flag"] = [0 for i in range(6)]
                dict_info["scaling_list_8x8"] = [[0 for j in range(64)] for i in range(2)]
                dict_info["use_default_scaling_matrix_8x8_flag"] = [0 for i in range(2)]
                for i in range(8):
                    dict_info["seq_scaling_list_present_flag"][i] = pyUtils.read_bits(str_payload, 1)
                    if dict_info["seq_scaling_list_present_flag"][i] == 1:
                        if i < 6:
                            pyUtils.scaling_list(str_payload, dict_info["scaling_list_4x4"][i], 16, dict_info["use_default_scaling_matrix_4x4_flag"][i])
                        else:
                            pyUtils.scaling_list(str_payload, dict_info["scaling_list_8x8"][i - 6], 64, dict_info["use_default_scaling_matrix_8x8_flag"][i - 6])
            dict_info["log2_max_frame_num_minus4"] = pyUtils.read_ue(str_payload)
            dict_info["pic_order_cnt_type"] = pyUtils.read_ue(str_payload)
            if dict_info["pic_order_cnt_type"] == 0:
                dict_info["log2_max_pic_order_cnt_lsb_minus4"] = pyUtils.read_ue(str_payload)
            elif dict_info["pic_order_cnt_type"] == 1:
                dict_info["delta_pic_order_always_zero_flag"] = pyUtils.read_bits(str_payload, 1)
                dict_info["offset_for_non_ref_pic"] = pyUtils.read_se(str_payload)
                dict_info["offset_for_top_to_bottom_field"] = pyUtils.read_se(str_payload)
                dict_info["num_ref_frames_in_pic_order_cnt_cycle"] = pyUtils.read_ue(str_payload)
                dict_info["offset_for_ref_frame"] = [0 for i in range(dict_info["num_ref_frames_in_pic_order_cnt_cycle"])]
                for i in range(dict_info["num_ref_frames_in_pic_order_cnt_cycle"]):
                    dict_info["offset_for_ref_frame"][i] = pyUtils.read_se(str_payload)
            dict_info["num_ref_frames"] = pyUtils.read_ue(str_payload)
            dict_info["gaps_in_frame_num_value_allowed_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["pic_width_in_mbs_minus1"] = pyUtils.read_ue(str_payload)
            dict_info["pic_height_in_map_units_minus1"] = pyUtils.read_ue(str_payload)
            dict_info["frame_mbs_only_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["frame_mbs_only_flag"] == 0:
                dict_info["mb_adaptive_frame_field_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["direct_8x8_inference_flag"] = pyUtils.read_bits(str_payload, 1)
            dict_info["frame_cropping_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["frame_cropping_flag"] == 1:
                dict_info["frame_crop_left_offset"] = pyUtils.read_ue(str_payload)
                dict_info["frame_crop_right_offset"] = pyUtils.read_ue(str_payload)
                dict_info["frame_crop_top_offset"] = pyUtils.read_ue(str_payload)
                dict_info["frame_crop_bottom_offset"] = pyUtils.read_ue(str_payload)
            dict_info["vui_parameters_present_flag"] = pyUtils.read_bits(str_payload, 1)
            if dict_info["vui_parameters_present_flag"] == 1:
                self.vui_parameters(str_payload)
            pyUtils.rbsp_trailing_bits(str_payload)

        # print("str_payload cur r_idx = " + str(str_payload.r_idx) + ", next bit = " + str(pyUtils.read_bits(str_payload, 1)))

    def print_info(self):
        print("sps info: ")
        pprint.pprint(self.dict_info)