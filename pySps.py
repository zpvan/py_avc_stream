# https://pythonhosted.org/bitstring/creation.html
# pip3.6.exe install bitstring // for windows
# pip3 install bitstring // for mac
from bitstring import BitStream, BitArray
import pyUtils 
import math

class Sps():

    def __init__(self, rbsp):
        self.rbsp = rbsp
        print("sps hex = " + self.rbsp.hex())
        self.Extended_SAR = 255

        self.profile_idc = 0
        self.constraint_set0_flag = 0
        self.constraint_set1_flag = 0
        self.constraint_set2_flag = 0
        self.constraint_set3_flag = 0
        self.reserved_zero_4bits = 0
        self.level_idc = 0
        self.seq_parameter_set_id = 0
        self.chroma_format_idc = 0
        self.residual_colour_transform_flag = 0
        self.bit_depth_luma_minus8 = 0
        self.bit_depth_chroma_minus8 = 0
        self.qpprime_y_zero_transform_bypass_flag = 0
        self.seq_scaling_matrix_present_flag = 0
        self.seq_scaling_list_present_flag = [0 for i in range(8)]
        self.scaling_list_4x4 = [[0 for j in range(16)] for i in range(6)]
        self.use_default_scaling_matrix_4x4_flag = [0 for i in range(6)]
        self.scaling_list_8x8 = [[0 for j in range(64)] for i in range(2)]
        self.use_default_scaling_matrix_8x8_flag = [0 for i in range(2)]
        self.log2_max_frame_num_minus4 = 0
        self.pic_order_cnt_type = 0
        self.log2_max_pic_order_cnt_lsb_minus4 = 0
        self.delta_pic_order_always_zero_flag = 0
        self.offset_for_non_ref_pic = 0
        self.offset_for_top_to_bottom_field = 0
        self.num_ref_frames_in_pic_order_cnt_cycle = 0
        self.offset_for_ref_frame = []
        self.num_ref_frames = 0
        self.gaps_in_frame_num_value_allowed_flag = 0
        self.pic_width_in_mbs_minus1 = 0
        self.pic_height_in_map_units_minus1 = 0
        self.frame_mbs_only_flag = 0
        self.mb_adaptive_frame_field_flag = 0
        self.direct_8x8_inference_flag = 0
        self.frame_cropping_flag = 0
        self.frame_crop_left_offset = 0
        self.frame_crop_right_offset = 0
        self.frame_crop_top_offset = 0
        self.frame_crop_bottom_offset = 0
        self.vui_parameters_present_flag = 0
        ##---vui_parameters---
        self.aspect_ratio_idc = 0
        self.sar_width = 0
        self.sar_height = 0
        self.overscan_appropriate_flag = 0
        self.video_format = 0
        self.video_full_range_flag = 0
        self.colour_primaries = 0
        self.transfer_characteristics = 0
        self.matrix_coefficients = 0
        self.chroma_sample_loc_type_top_field = 0
        self.chroma_sample_loc_type_bottom_field = 0
        self.num_units_in_tick = 0
        self.time_scale = 0
        self.fixed_frame_rate_flag = 0
        self.low_delay_hrd_flag = 0
        self.pic_struct_present_flag = 0
        self.motion_vectors_over_pic_boundaries_flag = 0
        self.max_bytes_per_pic_denom = 0
        self.max_bits_per_mb_denom = 0
        self.log2_max_mv_length_horizontal = 0
        self.log2_max_mv_length_vertical = 0
        self.num_reorder_frames = 0
        self.max_dec_frame_buffering = 0
        ##---hrd_parameters---
        self.cpb_cnt_minus1 = 0
        self.bit_rate_scale = 0
        self.cpb_size_scale = 0
        self.bit_rate_value_minus1 = []
        self.cpb_size_value_minus1 = []
        self.cbr_flag = []
        self.initial_cpb_removal_delay_length_minus1 = 0
        self.cpb_removal_delay_length_minus1 = 0
        self.dpb_output_delay_length_minus1 = 0
        self.time_offset_length = 0

    def hrd_parameters(self, str_payload):
        self.cpb_cnt_minus1 = pyUtils.read_ue(str_payload)
        self.bit_rate_scale = pyUtils.read_bits(str_payload, 4)
        self.cpb_size_scale = pyUtils.read_bits(str_payload, 4)
        schedse1idex = 0
        while schedse1idex <= self.cpb_cnt_minus1:
            self.bit_rate_value_minus1.append(pyUtils.read_ue(str_payload))
            self.cpb_size_value_minus1.append(pyUtils.read_ue(str_payload))
            self.cbr_flag.append(pyUtils.read_bits(str_payload, 1))
            schedse1idex = schedse1idex + 1
        self.initial_cpb_removal_delay_length_minus1 = pyUtils.read_bits(str_payload, 5)
        self.cpb_removal_delay_length_minus1 = pyUtils.read_bits(str_payload, 5)
        self.dpb_output_delay_length_minus1 = pyUtils.read_bits(str_payload, 5)
        self.time_offset_length = pyUtils.read_bits(str_payload, 5)

    def vui_parameters(self, str_payload):
        print("no implement vui_parameters() yet")
        aspect_ratio_info_present_flag = pyUtils.read_bits(str_payload, 1)
        if aspect_ratio_info_present_flag == 1:
            self.aspect_ratio_idc = pyUtils.read_bits(str_payload, 8)
            if self.aspect_ratio_idc == self.Extended_SAR:
                self.sar_width = pyUtils.read_bits(str_payload, 16)
                self.sar_height = pyUtils.read_bits(str_payload, 16)
        overscan_info_present_flag = pyUtils.read_bits(str_payload, 1)
        if overscan_info_present_flag == 1:
            self.overscan_appropriate_flag = pyUtils.read_bits(str_payload, 1)
        video_signal_type_present_flag = pyUtils.read_bits(str_payload, 1)
        if video_signal_type_present_flag == 1:
            self.video_format = pyUtils.read_bits(str_payload, 3)
            self.video_full_range_flag = pyUtils.read_bits(str_payload, 1)
            colour_description_present_flag = pyUtils.read_bits(str_payload, 1)
            if colour_description_present_flag == 1:
                self.colour_primaries = pyUtils.read_bits(str_payload, 8)
                self.transfer_characteristics = pyUtils.read_bits(str_payload, 8)
                self.matrix_coefficients = pyUtils.read_bits(str_payload, 8)
        chroma_loc_info_present_flag = pyUtils.read_bits(str_payload, 1)
        if chroma_loc_info_present_flag == 1:
            self.chroma_sample_loc_type_top_field = pyUtils.read_ue(str_payload)
            self.chroma_sample_loc_type_bottom_field = pyUtils.read_ue(str_payload)
        timing_info_present_flag = pyUtils.read_bits(str_payload, 1)
        if timing_info_present_flag == 1:
            self.num_units_in_tick = pyUtils.read_bits(str_payload, 32)
            self.time_scale = pyUtils.read_bits(str_payload, 32)
            self.fixed_frame_rate_flag = pyUtils.read_bits(str_payload, 1)
        nal_hrd_parameters_present_flag = pyUtils.read_bits(str_payload, 1)
        if nal_hrd_parameters_present_flag == 1:
            self.hrd_parameters(str_payload)
        vcl_hrd_parameters_present_flag = pyUtils.read_bits(str_payload, 1)
        if vcl_hrd_parameters_present_flag == 1:
            self.hrd_parameters(str_payload)
        if nal_hrd_parameters_present_flag == 1 or vcl_hrd_parameters_present_flag == 1:
            self.low_delay_hrd_flag = pyUtils.read_bits(str_payload, 1)
        self.pic_struct_present_flag = pyUtils.read_bits(str_payload, 1)
        bitstream_restriction_flag = pyUtils.read_bits(str_payload, 1)
        if bitstream_restriction_flag == 1:
            self.motion_vectors_over_pic_boundaries_flag = pyUtils.read_bits(str_payload, 1)
            self.max_bytes_per_pic_denom = pyUtils.read_ue(str_payload)
            self.max_bits_per_mb_denom = pyUtils.read_ue(str_payload)
            self.log2_max_mv_length_horizontal = pyUtils.read_ue(str_payload)
            self.log2_max_mv_length_vertical = pyUtils.read_ue(str_payload)
            self.num_reorder_frames = pyUtils.read_ue(str_payload)
            self.max_dec_frame_buffering = pyUtils.read_ue(str_payload)

    def parse(self):
        print("sps parse begin")
        
        str_sps_bin = BitArray(self.rbsp).bin
        print("sps binary = " + str_sps_bin)
        str_payload = pyUtils.StrBinArray(str_sps_bin)

        self.profile_idc = pyUtils.read_bits(str_payload, 8)
        self.constraint_set0_flag = pyUtils.read_bits(str_payload, 1)
        self.constraint_set1_flag = pyUtils.read_bits(str_payload, 1)
        self.constraint_set2_flag = pyUtils.read_bits(str_payload, 1)
        self.constraint_set3_flag = pyUtils.read_bits(str_payload, 1)
        self.reserved_zero_4bits = pyUtils.read_bits(str_payload, 4)
        self.level_idc = pyUtils.read_bits(str_payload, 8)
        self.seq_parameter_set_id = pyUtils.read_ue(str_payload)
        if (self.profile_idc == 100 or self.profile_idc == 110 or self.profile_idc == 122 or self.profile_idc == 144):
            self.chroma_format_idc = pyUtils.read_ue(str_payload)
            if self.chroma_format_idc == 3:
                self.residual_colour_transform_flag = pyUtils.read_bits(str_payload, 1)
            self.bit_depth_luma_minus8 = pyUtils.read_ue(str_payload)
            self.bit_depth_chroma_minus8 = pyUtils.read_ue(str_payload)
            self.qpprime_y_zero_transform_bypass_flag = pyUtils.read_bits(str_payload, 1)
            self.seq_scaling_matrix_present_flag = pyUtils.read_bits(str_payload, 1)
            if self.seq_scaling_matrix_present_flag == 1:
                i = 0
                while i < 8:
                    self.seq_scaling_list_present_flag[i] = pyUtils.read_bits(str_payload, 1)
                    if self.seq_scaling_list_present_flag[i] == 1:
                        if i < 6:
                            pyUtils.scaling_list(str_payload, self.scaling_list_4x4[i], 16, self.use_default_scaling_matrix_4x4_flag[i])
                        else:
                            pyUtils.scaling_list(str_payload, self.scaling_list_8x8[i - 6], 64,use_default_scaling_matrix_8x8_flag[i - 6])
                    i = i + 1
            self.log2_max_frame_num_minus4 = pyUtils.read_ue(str_payload)
            self.pic_order_cnt_type = pyUtils.read_ue(str_payload)
            if self.pic_order_cnt_type == 0:
                self.log2_max_pic_order_cnt_lsb_minus4 = pyUtils.read_ue(str_payload)
            elif self.pic_order_cnt_type == 1:
                self.delta_pic_order_always_zero_flag = pyUtils.read_bits(str_payload, 1)
                self.offset_for_non_ref_pic = pyUtils.read_se(str_payload)
                self.offset_for_top_to_bottom_field = pyUtils.read_se(str_payload)
                self.num_ref_frames_in_pic_order_cnt_cycle = pyUtils.read_ue(str_payload)
                i = 0
                while i < self.num_ref_frames_in_pic_order_cnt_cycle:
                    self.offset_for_ref_frame.append(pyUtils.read_se(str_payload))
            self.num_ref_frames = pyUtils.read_ue(str_payload)
            self.gaps_in_frame_num_value_allowed_flag = pyUtils.read_bits(str_payload, 1)
            self.pic_width_in_mbs_minus1 = pyUtils.read_ue(str_payload)
            self.pic_height_in_map_units_minus1 = pyUtils.read_ue(str_payload)
            self.frame_mbs_only_flag = pyUtils.read_bits(str_payload, 1)
            if self.frame_mbs_only_flag == 0:
                self.mb_adaptive_frame_field_flag = pyUtils.read_bits(str_payload, 1)
            self.direct_8x8_inference_flag = pyUtils.read_bits(str_payload, 1)
            self.frame_cropping_flag = pyUtils.read_bits(str_payload, 1)
            if self.frame_cropping_flag == 1:
                self.frame_crop_left_offset = pyUtils.read_ue(str_payload)
                self.frame_crop_right_offset = pyUtils.read_ue(str_payload)
                self.frame_crop_top_offset = pyUtils.read_ue(str_payload)
                self.frame_crop_bottom_offset = pyUtils.read_ue(str_payload)
            self.vui_parameters_present_flag = pyUtils.read_bits(str_payload, 1)
            if self.vui_parameters_present_flag == 1:
                self.vui_parameters(str_payload)
            pyUtils.rbsp_trailing_bits(str_payload)


        # print("str_payload cur r_idx = " + str(str_payload.r_idx) + ", next bit = " + str(pyUtils.read_bits(str_payload, 1)))

        print("sps parse end")

    def print_info(self):
        print("sps info: ")
        print("profile_idc int = " + str(self.profile_idc))
        print("constraint_set0_flag = " + str(self.constraint_set0_flag))
        print("constraint_set1_flag = " + str(self.constraint_set1_flag))
        print("constraint_set2_flag = " + str(self.constraint_set2_flag))
        print("constraint_set3_flag = " + str(self.constraint_set3_flag))
        print("reserved_zero_4bits = " + str(self.reserved_zero_4bits))
        print("level_idc = " + str(self.level_idc))
        print("seq_parameter_set_id = " + str(self.seq_parameter_set_id))
        print("chroma_format_idc = " + str(self.chroma_format_idc))
        print("residual_colour_transform_flag = " + str(self.residual_colour_transform_flag))
        print("bit_depth_luma_minus8 = " + str(self.bit_depth_luma_minus8))
        print("bit_depth_chroma_minus8 = " + str(self.bit_depth_chroma_minus8))
        print("qpprime_y_zero_transform_bypass_flag = " + str(self.qpprime_y_zero_transform_bypass_flag))
        print("seq_scaling_matrix_present_flag = " + str(self.seq_scaling_matrix_present_flag))
        print("seq_scaling_list_present_flag = " + str(self.seq_scaling_list_present_flag))
        print("scaling_list_4x4 = " + str(self.scaling_list_4x4))
        print("use_default_scaling_matrix_4x4_flag = " + str(self.use_default_scaling_matrix_4x4_flag))
        print("scaling_list_8x8 = " + str(self.scaling_list_8x8))
        print("use_default_scaling_matrix_8x8_flag = " + str(self.use_default_scaling_matrix_8x8_flag))
        print("log2_max_frame_num_minus4 = " + str(self.log2_max_frame_num_minus4))
        print("pic_order_cnt_type = " + str(self.pic_order_cnt_type))
        print("log2_max_pic_order_cnt_lsb_minus4 = " + str(self.log2_max_pic_order_cnt_lsb_minus4))
        print("delta_pic_order_always_zero_flag = " + str(self.delta_pic_order_always_zero_flag))
        print("offset_for_non_ref_pic = " + str(self.offset_for_non_ref_pic))
        print("offset_for_top_to_bottom_field = " + str(self.offset_for_top_to_bottom_field))
        print("num_ref_frames_in_pic_order_cnt_cycle = " + str(self.num_ref_frames_in_pic_order_cnt_cycle))
        print("offset_for_ref_frame = " + str(self.offset_for_ref_frame))
        print("num_ref_frames = " + str(self.num_ref_frames))
        print("gaps_in_frame_num_value_allowed_flag = " + str(self.gaps_in_frame_num_value_allowed_flag))
        print("pic_width_in_mbs_minus1 = " + str(self.pic_width_in_mbs_minus1))
        print("pic_height_in_map_units_minus1 = " + str(self.pic_height_in_map_units_minus1))
        print("frame_mbs_only_flag = " + str(self.frame_mbs_only_flag))
        print("mb_adaptive_frame_field_flag = " + str(self.mb_adaptive_frame_field_flag))
        print("direct_8x8_inference_flag = " + str(self.direct_8x8_inference_flag))
        print("frame_cropping_flag = " + str(self.frame_cropping_flag))
        print("frame_crop_left_offset = " + str(self.frame_crop_left_offset))
        print("frame_crop_right_offset = " + str(self.frame_crop_right_offset))
        print("frame_crop_top_offset = " + str(self.frame_crop_top_offset))
        print("frame_crop_bottom_offset = " + str(self.frame_crop_bottom_offset))
        print("vui_parameters_present_flag = " + str(self.vui_parameters_present_flag))
