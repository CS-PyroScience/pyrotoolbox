import unittest

import pandas as pd

from pyrotoolbox.parsers import read_workbench
from pyrotoolbox.oxygen import *
import numpy as np
import datetime
import os

script_dir = os.path.dirname(__file__)


class Test_i_only_think_in_hPa(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.5.3.2466/'

    def test_air_percentO2(self):
        file1 = '2024-09-03_170952_air_percentO2/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        hPa = i_only_think_in_hpa(df, m)
        self.assertAlmostEqual(hPa.iloc[1], 201.73488, 3)
        self.assertAlmostEqual(hPa.iloc[7], 201.68618, 3)

    def test_hPa(self):
        file1 = '2024-09-03_171034_air_hpa/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        hPa = i_only_think_in_hpa(df, m)
        self.assertAlmostEqual(hPa.iloc[1], 212.712, 3)
        self.assertAlmostEqual(hPa.iloc[6], 212.768, 3)

    def test_torr(self):
        self.maxDiff = None
        file1 = '2024-09-03_171110_air_torr/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        hPa = i_only_think_in_hpa(df, m)
        self.assertAlmostEqual(hPa.iloc[1], 201.336, 3)
        self.assertAlmostEqual(hPa.iloc[6], 201.364, 3)

    def test_airsat(self):
        file1 = '2024-09-03_171217_water_airsat/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        hPa = i_only_think_in_hpa(df, m)
        self.assertAlmostEqual(hPa.iloc[0], 202.62720079748, 3)
        self.assertAlmostEqual(hPa.iloc[5], 202.556710233018, 3)

    def test_mLL(self):
        file1 = '2024-09-03_171810_water_mLL/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        hPa = i_only_think_in_hpa(df, m)
        self.assertAlmostEqual(hPa.iloc[0], 191.283519, 3)
        self.assertAlmostEqual(hPa.iloc[5], 191.280425, 3)

    def test_uM(self):
        file1 = '2024-09-03_171911_water_uM/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        hPa = i_only_think_in_hpa(df, m)
        self.assertAlmostEqual(hPa.iloc[0], 191.274855930753, 3)
        self.assertAlmostEqual(hPa.iloc[5], 191.278988986348, 3)

    def test_mgL(self):
        file1 = '2024-09-03_172041_water_mgL/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        hPa = i_only_think_in_hpa(df, m)
        self.assertAlmostEqual(hPa.iloc[0], 191.139833287761, 3)
        self.assertAlmostEqual(hPa.iloc[5], 191.255517039212, 3)

    def test_ugL(self):
        file1 = '2024-09-03_172113_water_ugL/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        hPa = i_only_think_in_hpa(df, m)
        self.assertAlmostEqual(hPa.iloc[0], 191.262713941523, 3)
        self.assertAlmostEqual(hPa.iloc[5], 191.17831904096, 3)

    def test_airsat2(self):
        file1 = '2024-09-03_172218_water_airsat2/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        hPa = i_only_think_in_hpa(df, m)
        self.assertAlmostEqual(hPa.iloc[0], 191.070862223441, 3)
        self.assertAlmostEqual(hPa.iloc[5], 191.113457645337, 3)


class Test_convert_to_hPa(unittest.TestCase):
    data = pd.DataFrame({'oxygen_hPa': [191.12363250008, 46.2087176906861, 290.902510679616, 27.3718933986809,
                                        596.211100249724, 94.2940465382292],
                         'oxygen_torr': [143.354909542371, 34.6594843241821, 218.19542962123, 20.5306651555489,
                                         447.196336875927, 70.726546660138],
                         'oxygen_%airsat': [96.9287625596458, 27.8395804097788, 125.753657687437, 13.3805836800657,
                                           293.215927743013, 47.8206385420459],
                         'oxygen_%O2': [19.6225495379958, 5.76887861306943, 24.241875889968, 2.73718933986809,
                                        58.855982255649, 9.68111360762106],
                         'oxygen_µM': [224.209427053585, 83.5667195189217, 276.581287982379, 31.3049940158294,
                                       570.203249914319, 83.2724744623516],
                         'oxygen_mg/L': [7.17447745628766, 2.67405145788598, 8.85032463414814, 1.00172850351253,
                                         18.2459337940083, 2.66463591032079]})
    temperature = np.array([25.592, 5, 45, 20.123, 30, 25.584])
    pressure = np.array([974, 801, 1200, 1000, 1013, 974])
    salinity = np.array([10, 7, 3, 30, 35, 60])

    def test0(self):
        with self.assertRaises(TypeError):
            convert_to_hPa(pd.DataFrame())

    def test1(self):
        hpa = convert_to_hPa(self.data['oxygen_hPa'], unit='oxygen_hPa')
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_hPa'][i], hpa.iloc[i], 3)

    def test2(self):
        hpa = convert_to_hPa(self.data['oxygen_torr'], unit='oxygen_torr')
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_hPa'][i], hpa[i], 3)

    def test3(self):
        with self.assertRaises(ValueError):
            convert_to_hPa(self.data['oxygen_%airsat'], 'oxygen_%airsat')

    def test3_1(self):
        with self.assertRaises(ValueError):
            convert_to_hPa(self.data['oxygen_%airsat'], 'oxygen_%airsat', pressure=self.pressure)

    def test3_2(self):
        with self.assertRaises(ValueError):
            convert_to_hPa(self.data['oxygen_%airsat'], 'oxygen_%airsat', temperature=self.temperature)

    def test4(self):
        hpa = convert_to_hPa(self.data['oxygen_%airsat'], 'oxygen_%airsat', pressure=self.pressure,
                             temperature=self.temperature)
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_hPa'][i], hpa.iloc[i], 3)

    def test5(self):
        hpa = convert_to_hPa(self.data['oxygen_%O2'], 'oxygen_%O2', pressure=self.pressure)
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_hPa'][i], hpa.iloc[i], 3)

    def test6(self):
        with self.assertRaises(ValueError):
            convert_to_hPa(self.data['oxygen_µM'], 'oxygen_µM')
        with self.assertRaises(ValueError):
            convert_to_hPa(self.data['oxygen_µM'], 'oxygen_µM', pressure=self.pressure, temperature=self.temperature)
        with self.assertRaises(ValueError):
            convert_to_hPa(self.data['oxygen_µM'], 'oxygen_µM', salinity=self.salinity, pressure=self.pressure)

    def test7(self):
        hpa = convert_to_hPa(self.data['oxygen_µM'], 'oxygen_µM', pressure=self.pressure, temperature=self.temperature,
                             salinity=self.salinity)
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_hPa'][i], hpa.iloc[i], 3)

    def test8(self):
        with self.assertRaises(ValueError):
            convert_to_hPa(self.data['oxygen_mg/L'], 'oxygen_mg/L')
        with self.assertRaises(ValueError):
            convert_to_hPa(self.data['oxygen_mg/L'], 'oxygen_mg/L', pressure=self.pressure, temperature=self.temperature)
        with self.assertRaises(ValueError):
            convert_to_hPa(self.data['oxygen_mg/L'], 'oxygen_mg/L', salinity=self.salinity, pressure=self.pressure)

    def test9(self):
        hpa = convert_to_hPa(self.data['oxygen_mg/L'], 'oxygen_mg/L', pressure=self.pressure, temperature=self.temperature,
                             salinity=self.salinity)
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_hPa'][i], hpa.iloc[i], 3)


class Test_convert_from_hPa(unittest.TestCase):
    data = pd.DataFrame({'oxygen_hPa': [191.12363250008, 46.2087176906861, 290.902510679616, 27.3718933986809,
                                        596.211100249724, 94.2940465382292],
                         'oxygen_torr': [143.354909542371, 34.6594843241821, 218.19542962123, 20.5306651555489,
                                         447.196336875927, 70.726546660138],
                         'oxygen_%airsat': [96.9287625596458, 27.8395804097788, 125.753657687437, 13.3805836800657,
                                            293.215927743013, 47.8206385420459],
                         'oxygen_%O2': [19.6225495379958, 5.76887861306943, 24.241875889968, 2.73718933986809,
                                        58.855982255649, 9.68111360762106],
                         'oxygen_µM': [224.209427053585, 83.5667195189217, 276.581287982379, 31.3049940158294,
                                       570.203249914319, 83.2724744623516],
                         'oxygen_mg/L': [7.17447745628766, 2.67405145788598, 8.85032463414814, 1.00172850351253,
                                         18.2459337940083, 2.66463591032079]})
    temperature = np.array([25.592, 5, 45, 20.123, 30, 25.584])
    pressure = np.array([974, 801, 1200, 1000, 1013, 974])
    salinity = np.array([10, 7, 3, 30, 35, 60])

    def test_hPa_to_torr(self):
        torr = hPa_to_torr(self.data['oxygen_hPa'])
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_torr'][i], torr.iloc[i], 3)

    def test_hPa_to_percentO2(self):
        percentO2 = hPa_to_percentO2(self.data['oxygen_hPa'], self.pressure)
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_%O2'][i], percentO2.iloc[i], 3)

    def test_hPa_to_percent_airsat(self):
        percent_airsat = hPa_to_percent_airsat(self.data['oxygen_hPa'], self.pressure, self.temperature)
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_%airsat'][i], percent_airsat.iloc[i], 3)

    def test_hPa_to_uM(self):
        uM = hPa_to_uM(self.data['oxygen_hPa'], self.temperature, self.salinity)
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_µM'][i], uM.iloc[i], 3)

    def test_hPa_to_mgL(self):
        mgL = hPa_to_mgL(self.data['oxygen_hPa'], self.temperature, self.salinity)
        for i in range(len(self.data)):
            self.assertAlmostEqual(self.data['oxygen_mg/L'][i], mgL.iloc[i], 3)


if __name__ == '__main__':
    unittest.main()
