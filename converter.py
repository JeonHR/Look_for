import os
import openpyxl
from openpyxl import Workbook
import sys
import time
import shutil
import pandas as pd
import numpy as np


class converter:
    def __init__(self):
        self.savefilepath = './Con_Ex/exporter_output.csv'

    def converter(self):
        df_list = [] ## 열의 data 수집
        Log_dir = os.getcwd() + '\\Log'## \\의미는 \ 표시하기 위함
        filelist = self.target_csvfile(self.search(Log_dir))
        for file in filelist:
            df = pd.read_csv(file)
            df_drop = df.dropna(axis=0)  ## 행의 결측치 모두 제거
            df_list.append(df_drop)

        df_merge = pd.concat(df_list, axis=0) ## 행관련 합치는 효과
        df_merge.to_csv(self.savefilepath, index=False, mode='w')
        aaa = 1

    def search(self, folder_name, file_list=[]):
        file_list.clear()
        for (path, dir, files) in os.walk(folder_name): ###하위 항목 검색
            for filename in files:
                ext = os.path.splitext(filename)[-1]  ##[-1]을 통한 확장자만 구분
                if ext == '.csv' or ext == '.xlsx':
                    print("%s/%s" % (path, filename))## 문자열 입력
                    fullFilename = os.path.join(path, filename)
                    file_list.append(fullFilename)
        return file_list

    def target_csvfile(self, files, csvfile_list=[]):
        csvfile_list.clear()
        for file in files:
            if ".csv" in file:
                if "._" in file:
                    continue
                csvfile_list.append(file)
        return csvfile_list

if __name__ == '__main__':

    c = converter()
    c.converter()