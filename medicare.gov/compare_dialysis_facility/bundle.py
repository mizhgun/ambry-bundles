from ambry.bundle.loader import CsvBundle

class Bundle(CsvBundle):

    @staticmethod
    def int_na_caster(v):
        try:
            return int(v)
        except ValueError:
            return None
