from ambry.bundle.loader import CsvBundle
from datetime import datetime
import re
from collections import defaultdict

class Bundle(CsvBundle):
    re_assoc_date = re.compile(r'(\d{2}/\d{2}/\d{4})')
    col_nums = defaultdict(lambda: None)

    @staticmethod
    def int_na_caster(v):
        try:
            return int(v)
        except ValueError:
            return None

    @classmethod
    def association_date_caster(cls, v):
        if 'since' in v.lower():
            try:
                return datetime.strptime(cls.re_assoc_date.search(v).group(1), '%m/%d/%Y').date()
            except AttributeError:
                pass
        return None

    """
    Quick and dirty workaround - row padding (for empty lines)
    """
    def row_mangler(self, source, row_gen, row):
        # print "#####", row_gen.line_number, row[54]
        row_length, source_id = len(row), id(source)
        if self.col_nums[source_id] is None:
            self.col_nums[source_id] = row_length
        elif row_length < self.col_nums[source_id]:
            row += [''] * (self.col_nums[source_id] - row_length)
        return row