import re

from ambry.bundle.loader import CsvBundle


class Bundle(CsvBundle):
    RE_POINTS = re.compile('(\d+)\s+out\s+of\s+(\d+)', re.I)

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
            # print "***%s****" % v
            points = cls.RE_POINTS.search(v)
            # print points
            if points:
                return float(points.group(1))/float(points.group(2))
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