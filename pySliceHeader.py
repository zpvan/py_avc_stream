
import pyUtils
from bitstring import BitStream, BitArray

class SliceHeader():

    def __init__(self, rbsp, sps, pps, nalu_type, nal_ref_idc):
        self.rbsp = rbsp

        self.sps = sps
        self.pps = pps
        self.nalu_type = nalu_type
        self.nal_ref_idc = nal_ref_idc

        self.first_mb_in_slice = 0
        self.slice_type = 0
        self.pic_parameter_set_id = 0
        self.frame_num = 0
        self.field_pic_flag = 0
        self.bottom_field_flag = 0
        self.idr_pic_id = 0
        self.pic_order_cnt_lsb = 0
        self.delta_pic_order_cnt_bottom = 0
        self.delta_pic_order_cnt = []
        self.redundant_pic_cnt = 0
        self.direct_spatial_mv_pred_flag = 0
        self.num_ref_idx_active_override_flag = 0
        self.num_ref_idx_l0_active_minus1 = 0
        self.num_ref_idx_l1_active_minus1 = 0

        ##---ref_pic_list_reordering---
        self.ref_pic_list_reordering_flag_l0 = 0
        self.reordering_of_pic_nums_idc = 0
        self.abs_diff_pic_num_minus1 = 0
        self.long_term_pic_num = 0
        self.ref_pic_list_reordering_flag_l1 = 0

        ##---pred_weight_table---
        self.luma_log2_weight_denom = 0
        self.chroma_log2_weight_denom = 0
        self.luma_weight_l0_flag = 0
        self.luma_weight_l0 = []
        self.luma_offset_l0 = []
        self.chroma_weight_l0_flag = 0
        self.chroma_weight_l0 = []
        self.chroma_offset_l0 =[]
        self.luma_weight_l1_flag = 0
        self.luma_weight_l1 = []
        self.luma_offset_l1 = []
        self.chroma_weight_l1_flag = 0
        self.chroma_weight_l1 = []
        self.chroma_offset_l1 = []

        ##---dec_ref_pic_marking---
        self.no_output_of_prior_pics_flag = 0
        self.long_term_reference_flag = 0
        self.adaptive_ref_pic_marking_mode_flag = 0
        self.memory_management_control_operation = 0
        self.difference_of_pic_nums_minus1 = 0
        self.long_term_pic_num = 0
        self.long_term_frame_idx = 0
        self.max_long_term_frame_idx_plus1 = 0

        self.cabac_init_idc = 0
        self.slice_qp_delta = 0
        self.sp_for_switch_flag = 0
        self.slice_qs_delta = 0
        self.disable_deblocking_filter_idc = 0
        self.slice_alpha_c0_offset_div2 = 0
        self.slice_beta_offset_div2 = 0

    def ref_pic_list_reordering(self, str_payload):
        if (self.slice_type % 5) != 2 and (self.slice_type % 5) != 4:
            # slice_type != I and slice_type != SI
            self.ref_pic_list_reordering_flag_l0 = pyUtils.read_bits(str_payload, 1)
            if self.ref_pic_list_reordering_flag_l0 == 1:
                while self.reordering_of_pic_nums_idc != 3:
                    self.reordering_of_pic_nums_idc = pyUtils.read_ue(str_payload)
                    if self.reordering_of_pic_nums_idc == 0 or self.reordering_of_pic_nums_idc == 1:
                        self.abs_diff_pic_num_minus1 = pyUtils.read_ue(str_payload)
                    elif self.reordering_of_pic_nums_idc == 2:
                        self.long_term_pic_num = pyUtils.read_ue(str_payload)

        if (self.slice_type % 5) == 1:
            # slice_type == B
            self.ref_pic_list_reordering_flag_l1 = pyUtils.read_bits(str_payload, 1)
            if self.ref_pic_list_reordering_flag_l1 == 1:
                while self.reordering_of_pic_nums_idc != 3:
                    self.reordering_of_pic_nums_idc = pyUtils.read_ue(str_payload)
                    if self.reordering_of_pic_nums_idc == 0 or self.reordering_of_pic_nums_idc == 1:
                        self.abs_diff_pic_num_minus1 = pyUtils.read_ue(str_payload)
                    elif self.reordering_of_pic_nums_idc == 2:
                        self.long_term_pic_num = pyUtils.read_ue(str_payload)

    def pred_weight_table(self, str_payload):
        self.luma_log2_weight_denom = pyUtils.read_ue(str_payload)
        if self.sps.chroma_format_idc != 0:
            self.chroma_log2_weight_denom = pyUtils.read_ue(str_payload)
        i = 0
        while i <= self.num_ref_idx_l0_active_minus1:
            self.luma_weight_l0_flag = pyUtils.read_bits(str_payload, 1)
            if self.luma_weight_l0_flag == 1:
                self.luma_weight_l0.append(pyUtils.read_se(str_payload))
                self.luma_offset_l0.append(pyUtils.read_se(str_payload))
            if self.sps.chroma_format_idc != 0:
                self.chroma_weight_l0_flag = pyUtils.read_bits(str_payload, 1)
                if self.chroma_weight_l0_flag == 1:
                    for j in range(2):
                        self.chroma_weight_l0[i][j] = pyUtils.read_se(str_payload)
                        self.chroma_offset_l0[i][j] = pyUtils.read_se(str_payload)
            i = i + 1
        if (self.slice_type % 5) == 1:
            # slice_type == B
            for i in range(self.num_ref_idx_l1_active_minus1 + 1):
                self.luma_weight_l1_flag = pyUtils.read_bits(str_payload, 1)
                if self.luma_weight_l1_flag == 1:
                    self.luma_weight_l1.append(pyUtils.read_se(str_payload))
                    self.luma_offset_l1.append(pyUtils.read_se(str_payload))
                if self.sps.chroma_format_idc != 0:
                    self.chroma_weight_l1_flag = pyUtils.read_bits(str_payload, 1)
                    if self.chroma_weight_l1_flag == 1:
                        for j in range(2):
                            self.chroma_weight_l1[i][j] = pyUtils.read_se(str_payload)
                            self.chroma_offset_l1[i][j] = pyUtils.read_se(str_payload)

    def dec_ref_pic_marking(self, str_payload):
        if self.nalu_type == 5:
            self.no_output_of_prior_pics_flag = pyUtils.read_bits(str_payload, 1)
            self.long_term_reference_flag = pyUtils.read_bits(str_payload, 1)
        else:
            self.adaptive_ref_pic_marking_mode_flag = pyUtils.read_bits(str_payload, 1)
            if self.adaptive_ref_pic_marking_mode_flag == 1:
                self.memory_management_control_operation = 1
                while self.memory_management_control_operation != 0:
                    self.memory_management_control_operation = pyUtils.read_ue(str_payload)
                    if self.memory_management_control_operation == 1 or self.memory_management_control_operation == 3:
                        self.difference_of_pic_nums_minus1 = pyUtils.read_ue(str_payload)
                    if self.memory_management_control_operation == 2:
                        self.long_term_pic_num = pyUtils.read_ue(str_payload)
                    if self.memory_management_control_operation == 3 or self.memory_management_control_operation == 6:
                        self.long_term_frame_idx = pyUtils.read_ue(str_payload)
                    if self.memory_management_control_operation == 4:
                        self.max_long_term_frame_idx_plus1 = pyUtils.read_ue(str_payload)

    def parse(self):
        print("slice_header parse begin")

        str_slice_header_bin = BitArray(self.rbsp).bin
        # print("slice header binary = " + str_slice_header_bin)
        str_payload = pyUtils.StrBinArray(str_slice_header_bin)

        self.first_mb_in_slice = pyUtils.read_ue(str_payload)
        self.slice_type = pyUtils.read_ue(str_payload)
        self.pic_parameter_set_id = pyUtils.read_ue(str_payload)
        self.frame_num = pyUtils.read_bits(str_payload, self.sps.log2_max_frame_num_minus4 + 4)
        if self.sps.frame_mbs_only_flag == 0:
            self.field_pic_flag = pyUtils.read_bits(str_payload, 1)
            if self.field_pic_flag == 1:
                self.bottom_field_flag = pyUtils.read_bits(str_payload, 1)
        if self.nalu_type == 5:
            self.idr_pic_id = pyUtils.read_ue(str_payload)
        if self.sps.pic_order_cnt_type == 0:
            self.pic_order_cnt_lsb = pyUtils.read_bits(str_payload, self.sps.log2_max_pic_order_cnt_lsb_minus4 + 4)
            if self.pps.pic_order_present_flag == 1 and self.field_pic_flag == 0:
                self.delta_pic_order_cnt_bottom = pyUtils.read_se(str_payload)
        if self.sps.pic_order_cnt_type == 1 and self.sps.delta_pic_order_always_zero_flag == 0:
            self.delta_pic_order_cnt[0] = pyUtils.read_se(str_payload)
            if self.pps.pic_order_present_flag == 1 and self.field_pic_flag == 0:
                self.delta_pic_order_cnt[1] = pyUtils.read_se(str_payload)
        if self.pps.redundant_pic_cnt_present_flag == 1:
            self.redundant_pic_cnt = pyUtils.read_ue(str_payload)
        if (self.slice_type % 5) == 1:
            # slice_type == B
            self.direct_spatial_mv_pred_flag = pyUtils.read_bits(str_payload, 1)
        if (self.slice_type % 5) == 0 or (self.slice_type % 5) == 3 or (self.slice_type % 5) == 1:
            # slice_type == P or slice_type == SP or slice_type == B
            self.num_ref_idx_active_override_flag = pyUtils.read_bits(str_payload, 1)
            if self.num_ref_idx_active_override_flag == 1:
                self.num_ref_idx_l0_active_minus1 = pyUtils.read_ue(str_payload)
                if (self.slice_type % 5) == 1:
                    self.num_ref_idx_l1_active_minus1 = pyUtils.read_ue(str_payload)
        self.ref_pic_list_reordering(str_payload)
        if (self.pps.weighted_pred_flag == 1 and ((self.slice_type % 5) == 0 or (self.slice_type % 5) == 3)) or (self.pps.weighted_bipred_idc == 1 and (self.slice_type % 5) == 1):
            self.pred_weight_table(str_payload)
        if self.nal_ref_idc != 0:
            self.dec_ref_pic_marking(str_payload)
        if self.pps.entropy_coding_mode_flag == 1 and (self.slice_type % 5) != 2 and (self.slice_type % 5) != 4:
            self.cabac_init_idc = pyUtils.read_ue(str_payload)
        self.slice_qp_delta = pyUtils.read_se(str_payload)
        if (self.slice_type % 5) == 3 or (self.slice_type % 5) == 4:
            if (self.slice_type % 5) == 3:
                self.sp_for_switch_flag = pyUtils.read_bits(str_payload, 1)
            self.slice_qs_delta = pyUtils.read_se(str_payload)
        if self.pps.deblocking_filter_control_present_flag == 1:
            self.disable_deblocking_filter_idc = pyUtils.read_ue(str_payload)
            if self.disable_deblocking_filter_idc != 1:
                self.slice_alpha_c0_offset_div2 = pyUtils.read_se(str_payload)
                self.slice_beta_offset_div2 = pyUtils.read_se(str_payload)
        if self.pps.num_slice_groups_minus1 > 0 and self.slice_group_map_type >= 3 and slice_group_map_type <= 5:
            # self.slice_group_change_cycle = 
            pass

        print("slice_header parse begin")
        pass

    def print_info(self):
        print("first_mb_in_slice = " + str(self.first_mb_in_slice))
        print("slice_type = " + str(self.slice_type))
        print("pic_parameter_set_id = " + str(self.pic_parameter_set_id))
        print("frame_num = " + str(self.frame_num))
        print("field_pic_flag = " + str(self.field_pic_flag))
        print("bottom_field_flag = " + str(self.bottom_field_flag))
        print("idr_pic_id = " + str(self.idr_pic_id))
        print("pic_order_cnt_lsb = " + str(self.pic_order_cnt_lsb))
        print("delta_pic_order_cnt_bottom = " + str(self.delta_pic_order_cnt_bottom))
        print("delta_pic_order_cnt = " + str(self.delta_pic_order_cnt))
        print("redundant_pic_cnt = " + str(self.redundant_pic_cnt))
        print("direct_spatial_mv_pred_flag = " + str(self.direct_spatial_mv_pred_flag))
        print("num_ref_idx_active_override_flag = " + str(self.num_ref_idx_active_override_flag))
        print("num_ref_idx_l0_active_minus1 = " + str(self.num_ref_idx_l0_active_minus1))
        print("num_ref_idx_l1_active_minus1 = " + str(self.num_ref_idx_l1_active_minus1))
        print("ref_pic_list_reordering_flag_l0 = " + str(self.ref_pic_list_reordering_flag_l0))
        print("ref_pic_list_reordering_flag_l1 = " + str(self.ref_pic_list_reordering_flag_l1))
        print("reordering_of_pic_nums_idc = " + str(self.reordering_of_pic_nums_idc))
        print("abs_diff_pic_num_minus1 = " + str(self.abs_diff_pic_num_minus1))
        print("long_term_pic_num = " + str(self.long_term_pic_num))
        print("luma_log2_weight_denom = " + str(self.luma_log2_weight_denom))
        print("chroma_log2_weight_denom = " + str(self.chroma_log2_weight_denom))
        print("luma_weight_l0_flag = " + str(self.luma_weight_l0_flag))
        print("luma_weight_l0 = " + str(self.luma_weight_l0))
        print("luma_offset_l0 = " + str(self.luma_offset_l0))
        print("chroma_weight_l0_flag = " + str(self.chroma_weight_l0_flag))
        print("chroma_weight_l0 = " + str(self.chroma_weight_l0))
        print("chroma_offset_l0 = " + str(self.chroma_offset_l0))
        print("luma_weight_l1_flag = " + str(self.luma_weight_l1_flag))
        print("luma_weight_l1 = " + str(self.luma_weight_l1))
        print("luma_offset_l1 = " + str(self.luma_offset_l1))
        print("chroma_weight_l1_flag = " + str(self.chroma_weight_l1_flag))
        print("chroma_weight_l1 = " + str(self.chroma_weight_l1))
        print("chroma_offset_l1 = " + str(self.chroma_offset_l1))
        print("no_output_of_prior_pics_flag = " + str(self.no_output_of_prior_pics_flag))
        print("long_term_reference_flag = " + str(self.long_term_reference_flag))
        print("adaptive_ref_pic_marking_mode_flag = " + str(self.adaptive_ref_pic_marking_mode_flag))
        print("memory_management_control_operation = " + str(self.memory_management_control_operation))
        print("difference_of_pic_nums_minus1 = " + str(self.difference_of_pic_nums_minus1))
        print("long_term_pic_num = " + str(self.long_term_pic_num))
        print("long_term_frame_idx = " + str(self.long_term_frame_idx))
        print("max_long_term_frame_idx_plus1 = " + str(self.max_long_term_frame_idx_plus1))
        print("cabac_init_idc = " + str(self.cabac_init_idc))
        print("slice_qp_delta = " + str(self.slice_qp_delta))
        print("sp_for_switch_flag = " + str(self.sp_for_switch_flag))
        print("slice_qs_delta = " + str(self.slice_qs_delta))
        print("disable_deblocking_filter_idc = " + str(self.disable_deblocking_filter_idc))
        print("slice_alpha_c0_offset_div2 = " + str(self.slice_alpha_c0_offset_div2))
        print("slice_beta_offset_div2 = " + str(self.slice_beta_offset_div2))
        pass