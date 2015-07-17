import re

from ambry.bundle.loader import CsvBundle


class Bundle(CsvBundle):
    RE_POINTS = re.compile('(\d+)\s+out\s+of\s+(\d+)', re.I)

    out_of_fields = {
        "hvbp_hai_02_18_2015": (
            "scip_inf_1_achievement_points",
            "scip_inf_1_improvement_points",
            "scip_inf_1_measure_score",
            "scip_inf_2_achievement_points",
            "scip_inf_2_improvement_points",
            "scip_inf_2_measure_score",
            "scip_inf_3_achievement_points",
            "scip_inf_3_improvement_points",
            "scip_inf_3_measure_score",
            "scip_inf_4_achievement_points",
            "scip_inf_4_improvement_points",
            "scip_inf_4_measure_score",
            "scip_inf_9_achievement_points",
            "scip_inf_9_improvement_points",
            "scip_inf_9_measure_score"
        ),
        "hvbp_scip_02_18_2015": (
            "scip_card_2_achievement_points",
            "scip_card_2_improvement_points",
            "scip_card_2_measure_score",
            "scip_vte_2_achievement_points",
            "scip_vte_2_improvement_points",
            "scip_vte_2_measure_score",
        ),

        "hvbp_hf_02_18_2015":
            ("hf_1_achievement_points",
             "hf_1_improvement_points",
             "hf_1_measure_score",
             ),

        "hvbp_hcahps_02_18_2015":
            ("communication_with_nurses_achievement_points",
             "communication_with_nurses_improvement_points",
             "communication_with_nurses_dimension_score",
             "communication_with_doctors_achievement_points",
             "communication_with_doctors_improvement_points",
             "communication_with_doctors_dimension_score",
             "responsiveness_of_hospital_staff_achievement_points",
             "responsiveness_of_hospital_staff_improvement_points",
             "responsiveness_of_hospital_staff_dimension_score",
             "pain_management_achievement_points",
             "pain_management_improvement_points",
             "communication_about_medicines_achievement_points",
             "communication_about_medicines_improvement_points",
             "communication_about_medicines_dimension_score",
             "cleanliness_and_quietness_of_hospital_environment_achievement_points",
             "cleanliness_and_quietness_of_hospital_environment_improvement_points",
             "cleanliness_and_quietness_of_hospital_environment_dimension_score",
             "discharge_information_achievement_points",
             "discharge_information_improvement_points",
             "discharge_information_dimension_score",
             "overall_rating_of_hospital_achievement_points",
             "overall_rating_of_hospital_improvement_points",
             "overall_rating_of_hospital_dimension_score",
             ),

        "hvbp_efficiency_02_18_2015":
            ("mspb_1_achievement_points",
             "mspb_1_improvement_points",
             "mspb_1_measure_score",
             ),
        "hvbp_outcome_02_18_2015":
            ("mort_30_ami_achievement_points",
             "mort_30_ami_improvement_points",
             "mort_30_hf_achievement_points",
             "mort_30_hf_improvement_points",
             "mort_30_pn_achievement_points",
             "mort_30_pn_improvement_points",
             "mort_30_pn_measure_score",
             "psi_90_achievement_points",
             "psi_90_improvement_points",
             "psi_90_measure_score",
             "hai_1_achievement_points",
             "hai_1_improvement_points",
             ),

        "hvbp_pn_02_18_2015":
            ("pn_3b_achievement_points",
             "pn_3b_improvement_points",
             "pn_3b_measure_score",
             "pn_6_achievement_points",
             "pn_6_improvement_points",
             "pn_6_measure_score",
             ),
        "hvbp_ami_02_18_2015":
            ("ami_7a_achievement_points",
             "ami_7a_improvement_points",
             "ami_7a_measure_score",
             "ami_8a_achievement_points",
             "ami_8a_improvement_points",
             "ami_8a_measure_score",
             )
    }

    # def line_mangler(self, source, row_gen, l):
    #     return l.replace('\0', '')

    @staticmethod
    def int_na_caster(v):
        try:
            return int(v.replace(',', ''))
        except ValueError:
            return None

    @staticmethod
    def float_na_caster(v):
        try:
            return float(v)
        except ValueError:
            return None

    @classmethod
    def point_float_caster(cls, v):
        try:
            points = cls.RE_POINTS.search(v)
            if points:
                return float(points.group(1)) / float(points.group(2))
        except ValueError:
            pass
        return None

    @staticmethod
    def percent_float_caster(v):
        try:
            return float(v.rstrip('%'))
        except ValueError:
            return None

    @staticmethod
    def money_float_caster(v):
        try:
            return float(v.lstrip('$'))
        except ValueError:
            return None

    def build_modify_row(self, row_gen, p, source, row):
        out_of_map = self.out_of_fields.get(source.file, None)
        if out_of_map is not None:
            for field_name in out_of_map:
                v = row[field_name]
                row[field_name + '_nom'] = None
                row[field_name + '_denom'] = None
                try:
                    points = self.RE_POINTS.search(v)
                    if points:
                        row[field_name + '_nom'] = points.group(1)
                        row[field_name + '_denom'] = points.group(2)
                except ValueError:
                    pass
