

from bitstring import BitStream, BitArray
import pyUtils

class Pps():

    def __init__(self, rbsp):
        self.rbsp = rbsp
        print("pps hex = " + self.rbsp.hex())

        self.pic_parameter_set_id = 0
        self.seq_parameter_set_id = 0
        self.entropy_coding_mode_flag = 0
        self.pic_order_present_flag = 0
        self.num_slice_groups_minus1 = 0
        self.slice_group_map_type = 0
        self.run_length_minus1 = []
        self.top_left = []
        self.bottom_right = []
        self.slice_group_change_direction_flag = 0
        self.slice_group_change_rate_minus1 = 0
        self.pic_size_in_map_units_minus1 = 0
        self.slice_group_id = []
        self.num_ref_idx_l0_active_minus1 = 0
        self.num_ref_idx_l1_active_minus1 = 0
        self.weighted_pred_flag = 0
        self.weighted_bipred_idc = 0
        self.pic_init_qp_minus26 = 0
        self.pic_init_qs_minus26 = 0
        self.chroma_qp_index_offset = 0
        self.deblocking_filter_control_present_flag = 0
        self.constrained_intra_pred_flag = 0
        self.redundant_pic_cnt_present_flag = 0
        self.transform_8x8_mode_flag = 0
        self.pic_scaling_matrix_present_flag = 0
        self.pic_scaling_list_present_flag = []
        self.scaling_list_4x4 = [[0 for j in range(16)] for i in range(6)]
        self.use_default_scaling_matrix_4x4_flag = [0 for i in range(6)]
        self.scaling_list_8x8 = [[0 for j in range(64)] for i in range(2)]
        self.use_default_scaling_matrix_8x8_flag = [0 for i in range(2)]
        self.second_chroma_qp_index_offset = 0

    def parse(self):
        print("pps parse begin")

        str_pps_bin = BitArray(self.rbsp).bin
        print("pps binary = " + str_pps_bin)
        str_payload = pyUtils.StrBinArray(str_pps_bin)

        self.pic_parameter_set_id = pyUtils.read_ue(str_payload)
        self.seq_parameter_set_id = pyUtils.read_ue(str_payload)
        self.entropy_coding_mode_flag = pyUtils.read_bits(str_payload, 1)
        self.pic_order_present_flag = pyUtils.read_bits(str_payload, 1)
        self.num_slice_groups_minus1 = pyUtils.read_ue(str_payload)
        if self.num_slice_groups_minus1 > 0:
            self.slice_group_map_type = pyUtils.read_ue(str_payload)
            if self.slice_group_map_type == 0:
                i_group = 0
                while i_group <= self.num_slice_groups_minus1:
                    self.run_length_minus1.append(pyUtils.read_ue(str_payload))
                    i_group = i_group + 1
            elif self.slice_group_map_type == 2:
                i_group = 0
                while i_group < self.num_slice_groups_minus1:
                    self.top_left.append(pyUtils.read_ue(str_payload))
                    self.bottom_right.append(pyUtils.read_ue(str_payload))
                    i_group = i_group + 1
            elif self.slice_group_map_type == 3 or self.slice_group_map_type == 4 or self.slice_group_map_type == 5:
                self.slice_group_change_direction_flag = pyUtils.read_bits(str_payload, 1)
                self.slice_group_change_rate_minus1 = pyUtils.read_ue(str_payload)
            elif self.slice_group_map_type == 6:
                self.pic_size_in_map_units_minus1 = pyUtils.read_ue(str_payload)
                i = 0
                while i <= self.pic_size_in_map_units_minus1:
                    pass
                    i = i + 1
        self.num_ref_idx_l0_active_minus1 = pyUtils.read_ue(str_payload)
        self.num_ref_idx_l1_active_minus1 = pyUtils.read_ue(str_payload)
        self.weighted_pred_flag = pyUtils.read_bits(str_payload, 1)
        self.weighted_bipred_idc = pyUtils.read_bits(str_payload, 2)
        self.pic_init_qp_minus26 = pyUtils.read_se(str_payload)
        self.pic_init_qs_minus26 = pyUtils.read_se(str_payload)
        self.chroma_qp_index_offset = pyUtils.read_se(str_payload)
        self.deblocking_filter_control_present_flag = pyUtils.read_bits(str_payload, 1)
        self.constrained_intra_pred_flag = pyUtils.read_bits(str_payload, 1)
        self.redundant_pic_cnt_present_flag = pyUtils.read_bits(str_payload, 1)
        if pyUtils.more_rbsp_data(str_payload):
            self.transform_8x8_mode_flag = pyUtils.read_bits(str_payload, 1)
            self.pic_scaling_matrix_present_flag = pyUtils.read_bits(str_payload, 1)
            if self.pic_scaling_matrix_present_flag:
                i = 0
                while i < 6 + 2 * self.transform_8x8_mode_flag:
                    self.pic_scaling_list_present_flag.append(pyUtils.read_bits(str_payload, 1))
                    if self.pic_scaling_list_present_flag[i] == 1:
                        if i < 6:
                            pyUtils.scaling_list(str_payload, self.scaling_list_4x4[i], 16, self.use_default_scaling_matrix_4x4_flag[i])
                        else:
                            pyUtils.scaling_list(str_payload, self.scaling_list_8x8[i - 6], 64,use_default_scaling_matrix_8x8_flag[i - 6])
                    i = i + 1
            self.second_chroma_qp_index_offset = pyUtils.read_se(str_payload)
            pyUtils.rbsp_trailing_bits(str_payload)
                



        # print("str_payload cur r_idx = " + str(str_payload.r_idx) + ", next bit = " + str(pyUtils.read_bits(str_payload, 1)))
        print("pps parse end")

    def print_info(self):
        print("pic_parameter_set_id = " + str(self.pic_parameter_set_id))
        print("seq_parameter_set_id = " + str(self.seq_parameter_set_id))
        print("entropy_coding_mode_flag = " + str(self.entropy_coding_mode_flag))
        print("pic_order_present_flag = " + str(self.pic_order_present_flag))
        print("num_slice_groups_minus1 = " + str(self.num_slice_groups_minus1))
        print("slice_group_map_type = " + str(self.slice_group_map_type))
        print("run_length_minus1 = " + str(self.run_length_minus1))
        print("top_left = " + str(self.top_left))
        print("bottom_right = " + str(self.bottom_right))
        print("slice_group_change_direction_flag = " + str(self.slice_group_change_direction_flag))
        print("slice_group_change_rate_minus1 = " + str(self.slice_group_change_rate_minus1))
        print("pic_size_in_map_units_minus1 = " + str(self.pic_size_in_map_units_minus1))
        print("num_ref_idx_l0_active_minus1 = " + str(self.num_ref_idx_l0_active_minus1))
        print("num_ref_idx_l1_active_minus1 = " + str(self.num_ref_idx_l1_active_minus1))
        print("weighted_pred_flag = " + str(self.weighted_pred_flag))
        print("weighted_bipred_idc = " + str(self.weighted_bipred_idc))
        print("pic_init_qp_minus26 = " + str(self.pic_init_qp_minus26))
        print("pic_init_qs_minus26 = " + str(self.pic_init_qs_minus26))
        print("chroma_qp_index_offset = " + str(self.chroma_qp_index_offset))
        print("deblocking_filter_control_present_flag = " + str(self.deblocking_filter_control_present_flag))
        print("constrained_intra_pred_flag = " + str(self.constrained_intra_pred_flag))
        print("redundant_pic_cnt_present_flag = " + str(self.redundant_pic_cnt_present_flag))
        print("transform_8x8_mode_flag = " + str(self.transform_8x8_mode_flag))
        print("pic_scaling_matrix_present_flag = " + str(self.pic_scaling_matrix_present_flag))
        print("pic_scaling_list_present_flag = " + str(self.pic_scaling_list_present_flag))
        print("scaling_list_4x4 = " + str(self.scaling_list_4x4))
        print("use_default_scaling_matrix_4x4_flag = " + str(self.use_default_scaling_matrix_4x4_flag))
        print("scaling_list_8x8 = " + str(self.scaling_list_8x8))
        print("use_default_scaling_matrix_8x8_flag = " + str(self.use_default_scaling_matrix_8x8_flag))
        print("second_chroma_qp_index_offset = " + str(self.second_chroma_qp_index_offset))
