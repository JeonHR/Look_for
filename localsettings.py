import csv
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

class Local_Settings:
    def __init__(self):
        self.test_item = []
        self.sbin_item = []
        self.color_item = []
        self.edge_color_item = ''
        self.enable_edge = True

    def load_param(self):
        ret = {'TEST_ITEM': self.test_item,
               'SBIN_ITEM': self.sbin_item,
               'COLOR_ITEM': self.color_item,
               'ENABLE_EDGE': self.enable_edge,
               'EDGE_COLOR_ITEM': self.edge_color_item}
        return ret

    def load(self):
        get_current_path = os.getcwd()
        file_name = '{0}/Setting/localsettings.csv'.format(get_current_path)
        if not os.path.exists(file_name):
            return False

        f = open(file_name, 'r')
        rdr = csv.reader(f)

        for row in rdr:
            if row[0].lower().find('sbin') > -1:
                for i in row:
                    if 'sbin' in i.lower():
                        continue
                    self.sbin_item.append(i)

            elif row[0].lower().find('color') > -1:
                for i in row:
                    if 'color' in i.lower():
                        continue
                    self.color_item.append(i)

            elif row[0].lower().find('edge') > -1:
                if row[2].lower().find('enable') > -1:
                    self.enable_edge = True
                else:
                    self.enable_edge = False
                self.edge_color_item = row[1]

        return self.load_param()


if __name__ == "__main__":
    ls = Local_Settings()
    ret = ls.load()

