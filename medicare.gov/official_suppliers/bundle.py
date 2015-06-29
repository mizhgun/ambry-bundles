from ambry.bundle.loader import CsvBundle

class Bundle(CsvBundle):
    def line_mangler(self, source, row_gen, l):
        return l.replace('\0', '')
